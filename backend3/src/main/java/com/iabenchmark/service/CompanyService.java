package com.iabenchmark.service;

import com.iabenchmark.dto.CompanyRequest;
import com.iabenchmark.dto.CompanyResponse;
import com.iabenchmark.model.Company;
import com.iabenchmark.model.User;
import com.iabenchmark.repository.CompanyRepository;
import com.iabenchmark.repository.EvaluationRepository;
import com.iabenchmark.repository.UserRepository;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CompanyService {
    private final CompanyRepository companyRepository;
    private final UserRepository userRepository;
    private final EvaluationRepository evaluationRepository;

    public CompanyService(CompanyRepository companyRepository,
                          UserRepository userRepository,
                          EvaluationRepository evaluationRepository) {
        this.companyRepository = companyRepository;
        this.userRepository = userRepository;
        this.evaluationRepository = evaluationRepository;
    }

    public List<CompanyResponse> getAllCompanies() {
        return companyRepository.findAll().stream().map(this::toResponse).toList();
    }

    public CompanyResponse getCompanyById(Long id) {
        return toResponse(findCompany(id));
    }

    public CompanyResponse createCompany(CompanyRequest request) {
        if (companyRepository.existsByNameIgnoreCase(request.getName())) {
            throw new RuntimeException("Company name already exists");
        }

        Company company = new Company();
        applyRequest(company, request);
        return toResponse(companyRepository.save(company));
    }

    public CompanyResponse updateCompany(Long id, CompanyRequest request) {
        Company company = findCompany(id);
        boolean nameChanged = !company.getName().equalsIgnoreCase(request.getName());

        if (nameChanged && companyRepository.existsByNameIgnoreCase(request.getName())) {
            throw new RuntimeException("Company name already exists");
        }

        applyRequest(company, request);
        return toResponse(companyRepository.save(company));
    }

    public void deleteCompany(Long id) {
        Company company = findCompany(id);

        if (userRepository.existsByCompanyId(id)) {
            throw new RuntimeException("Impossible de supprimer cette entreprise car des utilisateurs y sont rattaches");
        }

        if (evaluationRepository.existsByCompanyId(id)) {
            throw new RuntimeException("Impossible de supprimer cette entreprise car des evaluations y sont rattachees");
        }

        companyRepository.delete(company);
    }

    private Company findCompany(Long id) {
        return companyRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Company not found with id: " + id));
    }

    private void applyRequest(Company company, CompanyRequest request) {
        company.setName(request.getName().trim());
        company.setSector(request.getSector().trim());
        company.setCountry(request.getCountry().trim());
        company.setSize(request.getSize().trim());
        company.setBusinessDomain(request.getBusinessDomain().trim());
        company.setWebsite(trimToNull(request.getWebsite()));
        company.setPhone(trimToNull(request.getPhone()));
        company.setEmail(trimToNull(request.getEmail()));
        company.setAddress(trimToNull(request.getAddress()));
    }

    private CompanyResponse toResponse(Company company) {
        User primaryContact = userRepository.findFirstByCompanyIdOrderByCreatedAtAsc(company.getId()).orElse(null);
        String email = company.getEmail() != null ? company.getEmail() : primaryContact != null ? primaryContact.getEmail() : null;
        String phone = company.getPhone() != null ? company.getPhone() : primaryContact != null ? primaryContact.getPhone() : null;

        return new CompanyResponse(
                company.getId(),
                company.getName(),
                company.getSector(),
                company.getCountry(),
                company.getSize(),
                company.getBusinessDomain(),
                company.getWebsite(),
                phone,
                email,
                company.getAddress(),
                company.getCreatedAt(),
                company.getUpdatedAt()
        );
    }

    private String trimToNull(String value) {
        if (value == null) {
            return null;
        }
        String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }
}
