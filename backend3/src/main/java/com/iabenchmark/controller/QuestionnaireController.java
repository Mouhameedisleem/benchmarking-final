package com.iabenchmark.controller;

import com.iabenchmark.dto.QuestionnaireRequest;
import com.iabenchmark.dto.QuestionnaireResponse;
import com.iabenchmark.service.ExcelImportService;
import com.iabenchmark.service.QuestionnaireService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/questionnaires")
@CrossOrigin(origins = "*")
public class QuestionnaireController {
    private final QuestionnaireService questionnaireService;
    private final ExcelImportService excelImportService;

    public QuestionnaireController(QuestionnaireService questionnaireService,
                                   ExcelImportService excelImportService) {
        this.questionnaireService = questionnaireService;
        this.excelImportService = excelImportService;
    }

    @GetMapping
    public ResponseEntity<List<QuestionnaireResponse>> getAllQuestionnaires() {
        return ResponseEntity.ok(questionnaireService.getAllQuestionnaires());
    }

    @GetMapping("/{id}")
    public ResponseEntity<QuestionnaireResponse> getQuestionnaireById(@PathVariable Long id) {
        return ResponseEntity.ok(questionnaireService.getQuestionnaireById(id));
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT', 'CLIENT')")
    public ResponseEntity<QuestionnaireResponse> createQuestionnaire(@Valid @RequestBody QuestionnaireRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(questionnaireService.createQuestionnaire(request));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<QuestionnaireResponse> updateQuestionnaire(@PathVariable Long id,
                                                                     @Valid @RequestBody QuestionnaireRequest request) {
        return ResponseEntity.ok(questionnaireService.updateQuestionnaire(id, request));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<Void> deleteQuestionnaire(@PathVariable Long id) {
        questionnaireService.deleteQuestionnaire(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/import")
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public ResponseEntity<?> importFromExcel(
            @RequestParam("file") MultipartFile file,
            @RequestParam("title") String title,
            @RequestParam("sector") String sector,
            @RequestParam("country") String country) {
        try {
            QuestionnaireResponse response = excelImportService.importFromExcel(file, title, sector, country);
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("message", e.getMessage()));
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("message", "Erreur lors de la lecture du fichier Excel: " + e.getMessage()));
        }
    }
}
