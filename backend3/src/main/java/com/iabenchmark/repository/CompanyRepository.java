package com.iabenchmark.repository;

import com.iabenchmark.model.Company;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface CompanyRepository extends JpaRepository<Company, Long> {
    boolean existsByNameIgnoreCase(String name);
    List<Company> findByConsultantId(Long consultantId);
}
