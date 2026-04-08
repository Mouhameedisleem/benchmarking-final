package com.iabenchmark.service;

import com.iabenchmark.dto.QuestionnaireResponse;
import com.iabenchmark.model.Question;
import com.iabenchmark.model.QuestionAxis;
import com.iabenchmark.model.Questionnaire;
import com.iabenchmark.model.QuestionnaireMode;
import com.iabenchmark.repository.QuestionnaireRepository;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class ExcelImportService {

    private final QuestionnaireRepository questionnaireRepository;
    private final QuestionnaireService questionnaireService;

    public ExcelImportService(QuestionnaireRepository questionnaireRepository,
                              QuestionnaireService questionnaireService) {
        this.questionnaireRepository = questionnaireRepository;
        this.questionnaireService = questionnaireService;
    }

    /**
     * Expected Excel format (row 1 = headers, rows 2+ = data):
     * | text | axis | subAxis | weight | displayOrder |
     *
     * axis values: BUSINESS, PROCESS, INFORMATION_SYSTEM
     */
    public QuestionnaireResponse importFromExcel(MultipartFile file,
                                                  String title,
                                                  String sector,
                                                  String country) throws IOException {
        if (file.isEmpty()) {
            throw new IllegalArgumentException("Le fichier Excel est vide");
        }

        List<Question> questions = parseExcel(file);
        if (questions.isEmpty()) {
            throw new IllegalArgumentException("Aucune question trouvée dans le fichier Excel");
        }

        Questionnaire questionnaire = new Questionnaire();
        questionnaire.setTitle(title);
        questionnaire.setDescription("Questionnaire importé via fichier Excel");
        questionnaire.setSector(sector);
        questionnaire.setCountry(country);
        questionnaire.setMode(QuestionnaireMode.IMPORTED);
        questionnaire.setActive(true);

        for (Question question : questions) {
            questionnaire.addQuestion(question);
        }

        Questionnaire saved = questionnaireRepository.save(questionnaire);
        return questionnaireService.getQuestionnaireById(saved.getId());
    }

    private List<Question> parseExcel(MultipartFile file) throws IOException {
        List<Question> questions = new ArrayList<>();

        try (Workbook workbook = new XSSFWorkbook(file.getInputStream())) {
            Sheet sheet = workbook.getSheetAt(0);
            int orderCounter = 1;

            for (int i = 1; i <= sheet.getLastRowNum(); i++) { // skip header row 0
                Row row = sheet.getRow(i);
                if (row == null || isRowEmpty(row)) continue;

                String text = getCellString(row, 0);
                if (text == null || text.isBlank()) continue;

                String axisStr  = getCellString(row, 1);
                String subAxis  = getCellString(row, 2);
                Integer weight  = getCellInt(row, 3, 1);
                Integer order   = getCellInt(row, 4, orderCounter);

                QuestionAxis axis = parseAxis(axisStr);

                Question question = new Question();
                question.setText(text.trim());
                question.setAxis(axis);
                question.setSubAxis(subAxis != null ? subAxis.trim() : "Général");
                question.setWeight(weight);
                question.setDisplayOrder(order);

                questions.add(question);
                orderCounter++;
            }
        }

        return questions;
    }

    private QuestionAxis parseAxis(String value) {
        if (value == null) return QuestionAxis.BUSINESS;
        return switch (value.trim().toUpperCase()) {
            case "PROCESS", "PROCESSUS"           -> QuestionAxis.PROCESS;
            case "INFORMATION_SYSTEM", "SI", "IS" -> QuestionAxis.INFORMATION_SYSTEM;
            default                               -> QuestionAxis.BUSINESS;
        };
    }

    private String getCellString(Row row, int col) {
        Cell cell = row.getCell(col, Row.MissingCellPolicy.RETURN_BLANK_AS_NULL);
        if (cell == null) return null;
        return switch (cell.getCellType()) {
            case STRING  -> cell.getStringCellValue();
            case NUMERIC -> String.valueOf((long) cell.getNumericCellValue());
            case BOOLEAN -> String.valueOf(cell.getBooleanCellValue());
            default      -> null;
        };
    }

    private Integer getCellInt(Row row, int col, int defaultVal) {
        Cell cell = row.getCell(col, Row.MissingCellPolicy.RETURN_BLANK_AS_NULL);
        if (cell == null) return defaultVal;
        return switch (cell.getCellType()) {
            case NUMERIC -> (int) cell.getNumericCellValue();
            case STRING  -> {
                try { yield Integer.parseInt(cell.getStringCellValue().trim()); }
                catch (NumberFormatException e) { yield defaultVal; }
            }
            default -> defaultVal;
        };
    }

    private boolean isRowEmpty(Row row) {
        for (int c = row.getFirstCellNum(); c < row.getLastCellNum(); c++) {
            Cell cell = row.getCell(c);
            if (cell != null && cell.getCellType() != CellType.BLANK) return false;
        }
        return true;
    }
}
