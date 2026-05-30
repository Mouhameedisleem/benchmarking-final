package com.iabenchmark.service;

import com.iabenchmark.dto.UserRequest;
import com.iabenchmark.dto.UserResponse;
import com.iabenchmark.model.Company;
import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.CompanyRepository;
import com.iabenchmark.repository.EvaluationRepository;
import com.iabenchmark.repository.UserRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;

@Service
public class UserManagementService {
    private final UserRepository userRepository;
    private final CompanyRepository companyRepository;
    private final EvaluationRepository evaluationRepository;
    private final PasswordEncoder passwordEncoder;

    public UserManagementService(UserRepository userRepository,
                                 CompanyRepository companyRepository,
                                 EvaluationRepository evaluationRepository,
                                 PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.companyRepository = companyRepository;
        this.evaluationRepository = evaluationRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public List<UserResponse> getAllUsers() {
        return userRepository.findAll().stream()
                .map(this::toResponse)
                .toList();
    }

    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + id));
        return toResponse(user);
    }

    public UserResponse createUser(UserRequest request) {
        validateCreateRequest(request);
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email deja utilise");
        }

        User user = new User();
        applyRequest(user, request, true);
        return toResponse(Objects.requireNonNull(userRepository.save(user)));
    }

    public UserResponse updateUser(Long id, UserRequest request) {
        User user = userRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + id));

        if (request.getEmail() == null || request.getEmail().trim().isEmpty()) {
            throw new RuntimeException("Email requis");
        }
        if (userRepository.existsByEmailAndIdNot(request.getEmail().trim(), id)) {
            throw new RuntimeException("Email deja utilise");
        }

        applyRequest(user, request, false);
        return toResponse(userRepository.save(Objects.requireNonNull(user)));
    }

    public UserResponse toggleUserStatus(Long id) {
        User user = userRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + id));
        user.setActive(!user.isActive());
        return toResponse(Objects.requireNonNull(userRepository.save(user)));
    }

    public void deleteUser(Long id) {
        User user = userRepository.findById(Objects.requireNonNull(id))
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + id));

        if (evaluationRepository.existsBySubmittedById(id)) {
            throw new RuntimeException("Impossible de supprimer cet utilisateur car il a deja soumis des evaluations");
        }

        userRepository.delete(Objects.requireNonNull(user));
    }

    private UserResponse toResponse(User user) {
        Long companyId = user.getCompany() != null ? user.getCompany().getId() : null;
        String companyName = user.getCompany() != null ? user.getCompany().getName() : null;
        java.time.LocalDateTime lastSeenAt = user.getLastLogin() != null
                ? user.getLastLogin()
                : user.getUpdatedAt() != null
                ? user.getUpdatedAt()
                : user.getCreatedAt();

        return new UserResponse(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getFirstName(),
                user.getLastName(),
                user.getRole().name(),
                companyId,
                companyName,
                user.getPhone(),
                user.isActive(),
                lastSeenAt,
                user.getCreatedAt(),
                user.getUpdatedAt()
        );
    }

    private void validateCreateRequest(UserRequest request) {
        if (request.getUsername() == null || request.getUsername().trim().isEmpty()) {
            throw new RuntimeException("Nom d'utilisateur requis");
        }
        if (request.getEmail() == null || request.getEmail().trim().isEmpty()) {
            throw new RuntimeException("Email requis");
        }
        if (request.getPassword() == null || request.getPassword().trim().isEmpty()) {
            throw new RuntimeException("Mot de passe requis");
        }
        if (request.getRole() == null || request.getRole().trim().isEmpty()) {
            throw new RuntimeException("Role requis");
        }
    }

    private void applyRequest(User user, UserRequest request, boolean isCreate) {
        user.setUsername(request.getUsername() != null ? request.getUsername().trim() : user.getUsername());
        user.setEmail(request.getEmail() != null ? request.getEmail().trim() : user.getEmail());
        user.setFirstName(request.getFirstName() != null ? request.getFirstName().trim() : user.getFirstName());
        user.setLastName(request.getLastName() != null ? request.getLastName().trim() : user.getLastName());
        user.setPhone(trimToNull(request.getPhone()));

        if (request.getRole() != null && !request.getRole().trim().isEmpty()) {
            user.setRole(Role.valueOf(request.getRole().trim().toUpperCase()));
        }

        if (isCreate && request.getPassword() != null) {
            user.setPassword(passwordEncoder.encode(request.getPassword()));
        }

        if (!isCreate && request.getPassword() != null && !request.getPassword().trim().isEmpty()) {
            user.setPassword(passwordEncoder.encode(request.getPassword()));
        }

        if (request.getCompanyId() != null) {
            Company company = companyRepository.findById(Objects.requireNonNull(request.getCompanyId()))
                    .orElseThrow(() -> new EntityNotFoundException("Company not found with id: " + request.getCompanyId()));
            user.setCompany(company);
        } else if (user.getRole() == Role.CLIENT) {
            user.setCompany(null);
        }

        if (request.getIsActive() != null) {
            user.setActive(request.getIsActive());
        } else if (isCreate) {
            user.setActive(true);
        }
    }

    private String trimToNull(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }
}
