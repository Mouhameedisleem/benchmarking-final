package com.iabenchmark.service;

import com.iabenchmark.dto.AuthResponse;
import com.iabenchmark.dto.ChangePasswordRequest;
import com.iabenchmark.dto.CompanyRegistrationRequest;
import com.iabenchmark.dto.ForgotPasswordRequest;
import com.iabenchmark.dto.LoginRequest;
import com.iabenchmark.dto.RegisterConsultantRequest;
import com.iabenchmark.dto.RegisterRequest;
import com.iabenchmark.dto.ResetPasswordRequest;
import com.iabenchmark.model.Company;
import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.CompanyRepository;
import com.iabenchmark.repository.UserRepository;
import com.iabenchmark.security.JwtUtils;
import com.iabenchmark.security.UserDetailsImpl;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Service
public class AuthService {
    // In-memory reset code store: email -> {code, expiry}
    private final Map<String, Object[]> resetCodes = new ConcurrentHashMap<>();

    @Autowired
    private AuthenticationManager authenticationManager;
    @Autowired
    private EmailService emailService;
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private CompanyRepository companyRepository;
    @Autowired
    private PasswordEncoder passwordEncoder;
    @Autowired
    private JwtUtils jwtUtils;

    public AuthResponse authenticateUser(LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getEmail(), loginRequest.getPassword()));
        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = jwtUtils.generateJwtToken(authentication);
        UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getPrincipal();
        List<String> roles = userDetails.getAuthorities().stream()
                .map(item -> item.getAuthority())
                .collect(Collectors.toList());
        User user = userRepository.findByEmail(userDetails.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));
        user.setLastLogin(LocalDateTime.now());
        user = userRepository.save(user);
        return toAuthResponse(jwt, user, roles);
    }

    public AuthResponse registerUser(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email dÃ©jÃ  utilisÃ©");
        }

        User user = new User(
                request.getUsername(),
                request.getEmail(),
                passwordEncoder.encode(request.getPassword()),
                request.getFirstName(),
                request.getLastName(),
                Role.valueOf(request.getRole())
        );

        if (request.getCompanyId() != null) {
            Company company = companyRepository.findById(request.getCompanyId())
                    .orElseThrow(() -> new EntityNotFoundException("Company not found with id: " + request.getCompanyId()));
            user.setCompany(company);
        }

        user.setPhone(request.getPhone());
        userRepository.save(user);

        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setEmail(request.getEmail());
        loginRequest.setPassword(request.getPassword());
        return authenticateUser(loginRequest);
    }

    public AuthResponse registerConsultant(RegisterConsultantRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email déjà utilisé");
        }
        User user = new User(
                request.getEmail(),
                request.getEmail(),
                passwordEncoder.encode(request.getPassword()),
                request.getFirstName(),
                request.getLastName(),
                Role.CONSULTANT
        );
        user.setPhone(request.getPhone());
        user.setActive(true);
        userRepository.save(user);

        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setEmail(request.getEmail());
        loginRequest.setPassword(request.getPassword());
        return authenticateUser(loginRequest);
    }

    public AuthResponse registerCompanyClient(CompanyRegistrationRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email dÃ©jÃ  utilisÃ©");
        }
        if (companyRepository.existsByNameIgnoreCase(request.getCompanyName())) {
            throw new RuntimeException("Company name already exists");
        }

        Company company = new Company();
        company.setName(request.getCompanyName().trim());
        company.setSector(request.getSector().trim());
        company.setCountry(request.getCountry().trim());
        company.setSize(request.getSize().trim());
        company.setBusinessDomain(request.getActivityDomain().trim());
        company.setEmail(request.getEmail() != null ? request.getEmail().trim() : null);
        company.setPhone(request.getPhone() != null ? request.getPhone().trim() : null);
        company.setWebsite(request.getWebsite() != null ? request.getWebsite().trim() : null);
        company.setAddress(request.getAddress() != null ? request.getAddress().trim() : null);
        company = companyRepository.save(company);

        RegisterRequest registerRequest = new RegisterRequest();
        registerRequest.setUsername(request.getEmail());
        registerRequest.setEmail(request.getEmail());
        registerRequest.setPassword(request.getPassword());
        registerRequest.setFirstName(request.getFirstName());
        registerRequest.setLastName(request.getLastName());
        registerRequest.setPhone(request.getPhone());
        registerRequest.setRole(Role.CLIENT.name());
        registerRequest.setCompanyId(company.getId());

        return registerUser(registerRequest);
    }

    public AuthResponse getCurrentUserProfile() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof UserDetailsImpl userDetails)) {
            throw new RuntimeException("Unauthorized");
        }

        User user = userRepository.findByEmail(userDetails.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));

        List<String> roles = user.getRole() == null
                ? List.of()
                : List.of("ROLE_" + user.getRole().name());

        return toAuthResponse(null, user, roles);
    }

    // ── Forgot password ──────────────────────────────────────────────────────────
    public String requestPasswordReset(ForgotPasswordRequest request) {
        userRepository.findByEmail(request.getEmail())
            .orElseThrow(() -> new EntityNotFoundException("Aucun compte trouvé avec cet email."));

        String code = String.format("%06d", new Random().nextInt(999999));
        resetCodes.put(request.getEmail(), new Object[]{code, LocalDateTime.now().plusMinutes(15)});

        emailService.sendPasswordResetCode(request.getEmail(), code);
        return code;
    }

    public void resetPassword(ResetPasswordRequest request) {
        Object[] entry = resetCodes.get(request.getEmail());
        if (entry == null) {
            throw new RuntimeException("Aucune demande de réinitialisation trouvée. Recommencez.");
        }
        String storedCode = (String) entry[0];
        LocalDateTime expiry = (LocalDateTime) entry[1];

        if (LocalDateTime.now().isAfter(expiry)) {
            resetCodes.remove(request.getEmail());
            throw new RuntimeException("Le code a expiré. Veuillez recommencer.");
        }
        if (!storedCode.equals(request.getCode())) {
            throw new RuntimeException("Code incorrect. Vérifiez le code reçu.");
        }

        User user = userRepository.findByEmail(request.getEmail())
            .orElseThrow(() -> new EntityNotFoundException("Utilisateur introuvable."));
        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        userRepository.save(user);
        resetCodes.remove(request.getEmail());
    }

    // ── Change password (authenticated) ──────────────────────────────────────────
    public void changePassword(ChangePasswordRequest request) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof UserDetailsImpl userDetails)) {
            throw new RuntimeException("Non authentifié.");
        }
        User user = userRepository.findByEmail(userDetails.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("Utilisateur introuvable."));

        if (!passwordEncoder.matches(request.getCurrentPassword(), user.getPassword())) {
            throw new BadCredentialsException("Mot de passe actuel incorrect.");
        }
        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        userRepository.save(user);
    }

    private AuthResponse toAuthResponse(String token, User user, List<String> roles) {
        Long companyId = user.getCompany() != null ? user.getCompany().getId() : null;
        String companyName = user.getCompany() != null ? user.getCompany().getName() : null;

        return new AuthResponse(
                token,
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getFirstName(),
                user.getLastName(),
                user.getRole() != null ? user.getRole().name() : null,
                companyId,
                companyName,
                roles
        );
    }
}
