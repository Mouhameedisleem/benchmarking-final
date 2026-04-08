package com.iabenchmark.security;

import com.iabenchmark.model.Role;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service("companySecurityService")
public class CompanySecurityService {
    private final UserRepository userRepository;

    public CompanySecurityService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public boolean canEditCompany(Long companyId) {
        User currentUser = getCurrentUser();
        if (currentUser == null) {
            return false;
        }

        if (currentUser.getRole() == Role.ADMIN || currentUser.getRole() == Role.CONSULTANT) {
            return true;
        }

        return currentUser.getRole() == Role.CLIENT
                && currentUser.getCompany() != null
                && companyId != null
                && companyId.equals(currentUser.getCompany().getId());
    }

    private User getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof UserDetailsImpl userDetails)) {
            return null;
        }

        return userRepository.findByEmail(userDetails.getEmail()).orElse(null);
    }
}
