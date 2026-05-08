package com.iabenchmark.repository;

import com.iabenchmark.model.Evaluation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface EvaluationRepository extends JpaRepository<Evaluation, Long> {
    List<Evaluation> findByCompanyId(Long companyId);
    List<Evaluation> findByPendingReviewTrueOrderByCreatedAtDesc();
    List<Evaluation> findByPendingReviewTrueAndCompanyConsultantIdOrderByCreatedAtDesc(Long consultantId);
    Evaluation findFirstByCompanyIdOrderByCreatedAtDesc(Long companyId);
    boolean existsByCompanyId(Long companyId);
    boolean existsBySubmittedById(Long userId);
}
