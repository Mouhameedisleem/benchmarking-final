package com.iabenchmark.repository;

import com.iabenchmark.model.ActionPlan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

public interface ActionPlanRepository extends JpaRepository<ActionPlan, Long> {

    List<ActionPlan> findByEvaluationIdOrderByPriorityAscCreatedAtAsc(Long evaluationId);

    boolean existsByEvaluationId(Long evaluationId);

    @Modifying
    @Transactional
    @Query("DELETE FROM ActionPlan a WHERE a.evaluation.id = :evaluationId")
    void deleteByEvaluationId(Long evaluationId);
}
