package com.iabenchmark.controller;

import com.iabenchmark.dto.CompanyRequest;
import com.iabenchmark.dto.CompanyResponse;
import com.iabenchmark.dto.CompanySetupRequest;
import com.iabenchmark.dto.CompanySetupResponse;
import com.iabenchmark.dto.QuestionResponse;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.UserRepository;
import com.iabenchmark.security.UserDetailsImpl;
import com.iabenchmark.service.CompanyService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequestMapping("/api/companies")
public class CompanyController {
    private final CompanyService companyService;
    private final UserRepository userRepository;

    public CompanyController(CompanyService companyService, UserRepository userRepository) {
        this.companyService = companyService;
        this.userRepository = userRepository;
    }

    @GetMapping
    public ResponseEntity<List<CompanyResponse>> getCompanies(@AuthenticationPrincipal UserDetailsImpl principal) {
        User user = resolveUser(principal);
        return ResponseEntity.ok(companyService.getCompaniesForUser(user));
    }

    @GetMapping("/{id}")
    public ResponseEntity<CompanyResponse> getCompanyById(@PathVariable Long id) {
        return ResponseEntity.ok(companyService.getCompanyById(id));
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<CompanyResponse> createCompany(
            @Valid @RequestBody CompanyRequest request,
            @AuthenticationPrincipal UserDetailsImpl principal) {
        User user = resolveUser(principal);
        return ResponseEntity.status(HttpStatus.CREATED).body(companyService.createCompany(request, user));
    }

    @PutMapping("/{id}")
    @PreAuthorize("@companySecurityService.canEditCompany(#id)")
    public ResponseEntity<CompanyResponse> updateCompany(@PathVariable Long id, @Valid @RequestBody CompanyRequest request) {
        return ResponseEntity.ok(companyService.updateCompany(id, request));
    }

    @GetMapping("/{id}/ai-questions")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<java.util.Map<String, Object>> getAiQuestions(@PathVariable Long id) {
        return ResponseEntity.ok()
                .header("Cache-Control", "no-store, no-cache, must-revalidate")
                .header("Pragma", "no-cache")
                .body(companyService.generateAiQuestions(id));
    }

    @GetMapping("/{id}/sector-questions")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<List<QuestionResponse>> getSectorQuestions(@PathVariable Long id) {
        return ResponseEntity.ok(companyService.getSectorQuestions(id));
    }

    @PostMapping("/{id}/finalize")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<CompanySetupResponse> finalizeSetup(
            @PathVariable Long id,
            @RequestBody CompanySetupRequest request) {
        return ResponseEntity.ok(companyService.finalizeSetup(id, request));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Void> deleteCompany(@PathVariable Long id) {
        companyService.deleteCompany(id);
        return ResponseEntity.noContent().build();
    }

    private User resolveUser(UserDetailsImpl principal) {
        if (principal == null) throw new EntityNotFoundException("Not authenticated");
        return userRepository.findByEmail(principal.getEmail())
                .orElseThrow(() -> new EntityNotFoundException("User not found"));
    }
}
