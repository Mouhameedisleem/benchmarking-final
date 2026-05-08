package com.iabenchmark.repository;

import com.iabenchmark.model.Questionnaire;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;
import java.util.Optional;

public interface QuestionnaireRepository extends JpaRepository<Questionnaire, Long> {

    // Returns all questionnaires for a company (avoids IncorrectResultSizeDataAccessException when multiple exist)
    List<Questionnaire> findByCompanyIdOrderByCreatedAtDesc(Long companyId);

    // Legacy single-result lookup used internally (safe only when uniqueness is guaranteed)
    Optional<Questionnaire> findFirstByCompanyIdOrderByCreatedAtDesc(Long companyId);

    @Query("SELECT DISTINCT q FROM Questionnaire q LEFT JOIN FETCH q.questions WHERE LOWER(q.sector) = LOWER(:sector)")
    List<Questionnaire> findBySectorIgnoreCaseWithQuestions(@Param("sector") String sector);
}
