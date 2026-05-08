package com.iabenchmark.service;

import com.iabenchmark.dto.BenchmarkResponse;
import com.iabenchmark.model.Evaluation;
import com.iabenchmark.model.EvaluationAnswer;
import com.iabenchmark.repository.EvaluationRepository;
import com.itextpdf.io.font.constants.StandardFonts;
import com.itextpdf.kernel.colors.ColorConstants;
import com.itextpdf.kernel.colors.DeviceRgb;
import com.itextpdf.kernel.font.PdfFont;
import com.itextpdf.kernel.font.PdfFontFactory;
import com.itextpdf.kernel.geom.PageSize;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.borders.Border;
import com.itextpdf.layout.borders.SolidBorder;
import com.itextpdf.layout.element.Cell;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.element.Text;
import com.itextpdf.layout.properties.TextAlignment;
import com.itextpdf.layout.properties.UnitValue;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.time.format.DateTimeFormatter;
import java.util.Comparator;
import java.util.List;

@Service
public class ReportService {

    private final EvaluationRepository evaluationRepository;
    private final RecommendationService recommendationService;
    private final AiService aiService;

    private static final DeviceRgb PRIMARY   = new DeviceRgb(23, 104, 229);
    private static final DeviceRgb DARK      = new DeviceRgb(15, 34, 66);
    private static final DeviceRgb LIGHT_BG  = new DeviceRgb(248, 250, 255);
    private static final DeviceRgb BORDER    = new DeviceRgb(217, 227, 239);
    private static final DeviceRgb SUCCESS   = new DeviceRgb(16, 150, 106);
    private static final DeviceRgb WARNING   = new DeviceRgb(245, 158, 11);
    private static final DeviceRgb DANGER    = new DeviceRgb(220, 38, 38);
    private static final DeviceRgb GRAY      = new DeviceRgb(107, 114, 128);

    public ReportService(EvaluationRepository evaluationRepository,
                         RecommendationService recommendationService,
                         AiService aiService) {
        this.evaluationRepository = evaluationRepository;
        this.recommendationService = recommendationService;
        this.aiService = aiService;
    }

    public byte[] generateEvaluationReport(Long evaluationId) {
        Evaluation evaluation = evaluationRepository.findById(evaluationId)
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        try {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            PdfWriter writer = new PdfWriter(out);
            PdfDocument pdf = new PdfDocument(writer);
            Document doc = new Document(pdf, PageSize.A4);
            doc.setMargins(40, 50, 40, 50);

            PdfFont bold   = PdfFontFactory.createFont(StandardFonts.HELVETICA_BOLD);
            PdfFont regular = PdfFontFactory.createFont(StandardFonts.HELVETICA);
            PdfFont italic  = PdfFontFactory.createFont(StandardFonts.HELVETICA_OBLIQUE);

            // ── Header banner ─────────────────────────────────────────────────
            Table header = new Table(UnitValue.createPercentArray(new float[]{2, 1})).useAllAvailableWidth();
            Cell leftCell = new Cell().setBorder(Border.NO_BORDER).setBackgroundColor(DARK).setPadding(20);
            leftCell.add(new Paragraph("IA Benchmark").setFont(bold).setFontSize(22).setFontColor(ColorConstants.WHITE));
            leftCell.add(new Paragraph("Rapport de maturité digitale").setFont(regular).setFontSize(11)
                    .setFontColor(new DeviceRgb(180, 200, 240)));
            header.addCell(leftCell);

            Cell rightCell = new Cell().setBorder(Border.NO_BORDER).setBackgroundColor(PRIMARY).setPadding(20)
                    .setTextAlignment(TextAlignment.RIGHT);
            rightCell.add(new Paragraph(evaluation.getCompany().getName())
                    .setFont(bold).setFontSize(14).setFontColor(ColorConstants.WHITE));
            rightCell.add(new Paragraph(evaluation.getCompany().getSector() != null ? evaluation.getCompany().getSector() : "")
                    .setFont(regular).setFontSize(10).setFontColor(new DeviceRgb(200, 220, 255)));
            if (evaluation.getCreatedAt() != null) {
                rightCell.add(new Paragraph(evaluation.getCreatedAt().format(DateTimeFormatter.ofPattern("dd/MM/yyyy")))
                        .setFont(regular).setFontSize(10).setFontColor(new DeviceRgb(200, 220, 255)));
            }
            header.addCell(rightCell);
            doc.add(header);
            doc.add(spacer(16));

            // ── Score global ──────────────────────────────────────────────────
            doc.add(sectionTitle("Score Global de Maturité Digitale", bold));

            Table scoreTable = new Table(UnitValue.createPercentArray(new float[]{1, 1, 1, 1})).useAllAvailableWidth();
            scoreTable.addCell(scoreCell("Score Global", fmt(evaluation.getGlobalScore()) + "/100", PRIMARY, bold, regular));
            scoreTable.addCell(scoreCell("Axe Métier", fmt(evaluation.getBusinessScore()) + "/100", new DeviceRgb(23, 104, 229), bold, regular));
            scoreTable.addCell(scoreCell("Axe Processus", fmt(evaluation.getProcessScore()) + "/100", SUCCESS, bold, regular));
            scoreTable.addCell(scoreCell("Axe SI", fmt(evaluation.getInformationSystemScore()) + "/100", new DeviceRgb(14, 165, 233), bold, regular));
            doc.add(scoreTable);
            doc.add(spacer(8));

            // Maturity level badge
            String maturity = evaluation.getMaturityLevel().name();
            DeviceRgb matColor = maturityColor(maturity);
            doc.add(new Paragraph("Niveau de maturité : " + maturity)
                    .setFont(bold).setFontSize(12).setFontColor(matColor)
                    .setBackgroundColor(maturityBg(maturity))
                    .setPadding(8).setBorderRadius(new com.itextpdf.layout.properties.BorderRadius(8)));
            doc.add(spacer(16));

            // ── Synthèse par axe ─────────────────────────────────────────────
            doc.add(sectionTitle("Synthèse par Axe", bold));
            String[] axes = {"METIER", "PROCESSUS", "SI"};
            double[] axisScores = {evaluation.getBusinessScore(), evaluation.getProcessScore(), evaluation.getInformationSystemScore()};
            String[] axisLabels = {"Axe Métier (Business)", "Axe Processus", "Axe Système d'Information"};

            for (int i = 0; i < axes.length; i++) {
                Table axisRow = new Table(UnitValue.createPercentArray(new float[]{1, 4})).useAllAvailableWidth();
                Cell scoreCol = new Cell().setBackgroundColor(LIGHT_BG).setBorder(new SolidBorder(BORDER, 1))
                        .setPadding(12).setTextAlignment(TextAlignment.CENTER);
                scoreCol.add(new Paragraph(axisLabels[i]).setFont(bold).setFontSize(9).setFontColor(GRAY));
                scoreCol.add(new Paragraph(fmt(axisScores[i]) + "/100").setFont(bold).setFontSize(18).setFontColor(PRIMARY));
                axisRow.addCell(scoreCol);
                Cell descCol = new Cell().setBorder(new SolidBorder(BORDER, 1)).setPadding(12);
                descCol.add(new Paragraph(buildAxisSummaryText(axes[i], axisScores[i])).setFont(regular).setFontSize(10).setFontColor(DARK));
                axisRow.addCell(descCol);
                doc.add(axisRow);
                doc.add(spacer(6));
            }
            doc.add(spacer(10));

            // ── Détail par sous-axe ───────────────────────────────────────────
            List<EvaluationAnswer> sorted = evaluation.getResponses().stream()
                    .sorted(Comparator.comparing(a -> a.getQuestion().getDisplayOrder()))
                    .toList();

            if (!sorted.isEmpty()) {
                doc.add(sectionTitle("Détail des Réponses", bold));
                Table table = new Table(UnitValue.createPercentArray(new float[]{4, 1, 1, 1, 1})).useAllAvailableWidth();
                // Headers
                for (String h : new String[]{"Question", "Axe", "Sous-axe", "Réponse", "Score"}) {
                    table.addHeaderCell(new Cell().setBackgroundColor(DARK).setPadding(6)
                            .add(new Paragraph(h).setFont(bold).setFontSize(9).setFontColor(ColorConstants.WHITE)));
                }
                boolean alt = false;
                for (EvaluationAnswer a : sorted) {
                    DeviceRgb rowBg = alt ? LIGHT_BG : new DeviceRgb(255, 255, 255);
                    double normalized = Math.round((a.getScoreValue() / 5.0) * 100.0);
                    table.addCell(new Cell().setBackgroundColor(rowBg).setPadding(5)
                            .add(new Paragraph(a.getQuestion().getText()).setFont(regular).setFontSize(8)));
                    table.addCell(new Cell().setBackgroundColor(rowBg).setPadding(5).setTextAlignment(TextAlignment.CENTER)
                            .add(new Paragraph(axisLabel(a.getQuestion().getAxis().name())).setFont(regular).setFontSize(8)));
                    table.addCell(new Cell().setBackgroundColor(rowBg).setPadding(5)
                            .add(new Paragraph(a.getQuestion().getSubAxis() != null ? a.getQuestion().getSubAxis() : "").setFont(regular).setFontSize(8)));
                    table.addCell(new Cell().setBackgroundColor(rowBg).setPadding(5).setTextAlignment(TextAlignment.CENTER)
                            .add(new Paragraph(a.getScoreValue().intValue() + "/5").setFont(bold).setFontSize(9)));
                    DeviceRgb scoreColor = normalized >= 75 ? SUCCESS : normalized >= 50 ? PRIMARY : normalized >= 25 ? WARNING : DANGER;
                    table.addCell(new Cell().setBackgroundColor(rowBg).setPadding(5).setTextAlignment(TextAlignment.CENTER)
                            .add(new Paragraph((int)normalized + "").setFont(bold).setFontSize(9).setFontColor(scoreColor)));
                    alt = !alt;
                }
                doc.add(table);
                doc.add(spacer(16));
            }

            // ── Recommandations ───────────────────────────────────────────────
            doc.add(sectionTitle("Recommandations", bold));
            var recommendations = getRecommendations(evaluationId);

            for (var rec : recommendations) {
                DeviceRgb pColor = "HAUTE".equals(rec.getPriority()) ? DANGER :
                                   "MOYENNE".equals(rec.getPriority()) ? WARNING : SUCCESS;
                Table recTable = new Table(UnitValue.createPercentArray(new float[]{1})).useAllAvailableWidth();
                Cell recCell = new Cell().setBorder(new SolidBorder(pColor, 2)).setBorderLeft(new SolidBorder(pColor, 5))
                        .setPadding(12).setMarginBottom(6);
                recCell.add(new Paragraph()
                        .add(new Text("[" + rec.getPriority() + "] ").setFont(bold).setFontSize(9).setFontColor(pColor))
                        .add(new Text(rec.getAxis()).setFont(bold).setFontSize(9).setFontColor(GRAY)));
                recCell.add(new Paragraph(rec.getTitle()).setFont(bold).setFontSize(11).setFontColor(DARK));
                recCell.add(new Paragraph(rec.getDescription()).setFont(regular).setFontSize(9).setFontColor(GRAY).setMarginTop(4));
                if (rec.getBestPractice() != null && !rec.getBestPractice().isBlank()) {
                    recCell.add(new Paragraph("Référence : " + rec.getBestPractice())
                            .setFont(italic).setFontSize(8).setFontColor(GRAY).setMarginTop(4));
                }
                recTable.addCell(recCell);
                doc.add(recTable);
                doc.add(spacer(4));
            }

            // ── Benchmarking Sectoriel ────────────────────────────────────────
            if (aiService.isAiServiceAvailable()) {
                try {
                    BenchmarkResponse benchmark = aiService.getBenchmark(evaluationId);
                    addBenchmarkSection(doc, benchmark, bold, regular, italic);
                } catch (Exception ignored) {}
            }

            // ── Footer ────────────────────────────────────────────────────────
            doc.add(spacer(20));
            doc.add(new Paragraph("Rapport généré par IA Benchmark — Fondé sur Gartner, McKinsey, ISO 27001, CMMI, COBIT, WEF DTI")
                    .setFont(italic).setFontSize(8).setFontColor(GRAY).setTextAlignment(TextAlignment.CENTER));

            doc.close();
            return out.toByteArray();

        } catch (Exception e) {
            throw new RuntimeException("Erreur lors de la génération du rapport PDF: " + e.getMessage(), e);
        }
    }

    private void addBenchmarkSection(Document doc, BenchmarkResponse bm,
            PdfFont bold, PdfFont regular, PdfFont italic) throws Exception {

        doc.add(spacer(16));
        doc.add(sectionTitle("Benchmarking Sectoriel", bold));

        // Executive summary
        if (bm.getExecutiveSummary() != null && !bm.getExecutiveSummary().isBlank()) {
            doc.add(new Paragraph(bm.getExecutiveSummary())
                .setFont(regular).setFontSize(10).setFontColor(DARK)
                .setBackgroundColor(LIGHT_BG)
                .setBorder(new SolidBorder(BORDER, 1))
                .setPadding(10).setMarginBottom(12));
        }

        // Sector positioning KPI table
        if (bm.getSectorBenchmark() != null) {
            doc.add(new Paragraph("Positionnement Sectoriel")
                .setFont(bold).setFontSize(11).setFontColor(DARK).setMarginBottom(6));
            BenchmarkResponse.SectorBenchmark sb = bm.getSectorBenchmark();
            Table kpiTable = new Table(UnitValue.createPercentArray(new float[]{1,1,1,1})).useAllAvailableWidth();
            kpiTable.addCell(scoreCell("Score Entreprise", fmt(bm.getGlobalScore()) + "/100", PRIMARY, bold, regular));
            kpiTable.addCell(scoreCell("Moyenne Nationale", fmt(sb.getNationalAverage()) + "/100", GRAY, bold, regular));
            kpiTable.addCell(scoreCell("Moyenne Internationale", fmt(sb.getInternationalAverage()) + "/100", new DeviceRgb(14, 165, 233), bold, regular));
            kpiTable.addCell(scoreCell("Top Quartile", fmt(sb.getTopQuartileScore()) + "/100", SUCCESS, bold, regular));
            doc.add(kpiTable);
            doc.add(spacer(6));
            String info = "Percentile : " + sb.getCompanyPercentile() + "ème"
                + (sb.getPositioningLabel() != null && !sb.getPositioningLabel().isBlank() ? "  |  " + sb.getPositioningLabel() : "")
                + (sb.getSource() != null && !sb.getSource().isBlank() ? "  |  Source : " + sb.getSource() : "");
            doc.add(new Paragraph(info).setFont(italic).setFontSize(9).setFontColor(GRAY).setMarginBottom(12));
        }

        // Axis benchmarks table
        if (bm.getAxisBenchmarks() != null && !bm.getAxisBenchmarks().isEmpty()) {
            doc.add(new Paragraph("Benchmarking par Axe")
                .setFont(bold).setFontSize(11).setFontColor(DARK).setMarginBottom(6));
            Table axisTable = new Table(UnitValue.createPercentArray(new float[]{2,1,1,1,1,1})).useAllAvailableWidth();
            for (String h : new String[]{"Axe", "Score", "Moy. Secteur", "Top Quartile", "Écart/Moy.", "Écart/Top"}) {
                axisTable.addHeaderCell(new Cell().setBackgroundColor(DARK).setPadding(6)
                    .add(new Paragraph(h).setFont(bold).setFontSize(9).setFontColor(ColorConstants.WHITE)));
            }
            boolean alt = false;
            for (BenchmarkResponse.AxisBenchmark ab : bm.getAxisBenchmarks()) {
                DeviceRgb rowBg = alt ? LIGHT_BG : new DeviceRgb(255,255,255);
                String label = ab.getAxisLabel() != null && !ab.getAxisLabel().isBlank() ? ab.getAxisLabel() : ab.getAxis();
                axisTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6)
                    .add(new Paragraph(label).setFont(bold).setFontSize(9).setFontColor(DARK)));
                axisTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6).setTextAlignment(TextAlignment.CENTER)
                    .add(new Paragraph(fmt(ab.getCompanyScore())).setFont(bold).setFontSize(9).setFontColor(PRIMARY)));
                axisTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6).setTextAlignment(TextAlignment.CENTER)
                    .add(new Paragraph(fmt(ab.getSectorAverage())).setFont(regular).setFontSize(9)));
                axisTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6).setTextAlignment(TextAlignment.CENTER)
                    .add(new Paragraph(fmt(ab.getTopQuartile())).setFont(regular).setFontSize(9).setFontColor(SUCCESS)));
                double gapAvg = ab.getGapToAverage() != null ? ab.getGapToAverage() : 0.0;
                double gapTop = ab.getGapToTop() != null ? ab.getGapToTop() : 0.0;
                axisTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6).setTextAlignment(TextAlignment.CENTER)
                    .add(new Paragraph((gapAvg >= 0 ? "+" : "") + fmt(gapAvg))
                        .setFont(bold).setFontSize(9).setFontColor(gapAvg >= 0 ? SUCCESS : DANGER)));
                axisTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6).setTextAlignment(TextAlignment.CENTER)
                    .add(new Paragraph((gapTop >= 0 ? "+" : "") + fmt(gapTop))
                        .setFont(bold).setFontSize(9).setFontColor(gapTop >= 0 ? SUCCESS : WARNING)));
                alt = !alt;
            }
            doc.add(axisTable);
            doc.add(spacer(12));
        }

        // Trends
        if (bm.getTrends() != null && !bm.getTrends().isEmpty()) {
            doc.add(new Paragraph("Tendances Sectorielles")
                .setFont(bold).setFontSize(11).setFontColor(DARK).setMarginBottom(6));
            for (BenchmarkResponse.BenchmarkTrend t : bm.getTrends()) {
                String impact = t.getImpactLevel() != null ? t.getImpactLevel().toUpperCase() : "";
                DeviceRgb impColor = impact.contains("HIGH") || impact.contains("ELEV") ? DANGER
                    : impact.contains("MED") || impact.contains("MOY") ? WARNING : SUCCESS;
                Table tTable = new Table(UnitValue.createPercentArray(new float[]{1})).useAllAvailableWidth();
                Cell tCell = new Cell().setBorder(Border.NO_BORDER).setBorderLeft(new SolidBorder(impColor, 4))
                    .setBackgroundColor(LIGHT_BG).setPadding(10).setMarginBottom(6);
                tCell.add(new Paragraph()
                    .add(new Text(t.getTitle() != null ? t.getTitle() : "").setFont(bold).setFontSize(10).setFontColor(DARK))
                    .add(new Text("  [" + impact + " — " + (t.getHorizon() != null ? t.getHorizon() : "") + "]")
                        .setFont(italic).setFontSize(8).setFontColor(GRAY)));
                if (t.getDescription() != null && !t.getDescription().isBlank()) {
                    tCell.add(new Paragraph(t.getDescription()).setFont(regular).setFontSize(9).setFontColor(GRAY).setMarginTop(4));
                }
                if (t.getAdoptionRate() != null && !t.getAdoptionRate().isBlank()) {
                    tCell.add(new Paragraph("Taux d'adoption : " + t.getAdoptionRate())
                        .setFont(italic).setFontSize(8).setFontColor(GRAY).setMarginTop(2));
                }
                tTable.addCell(tCell);
                doc.add(tTable);
                doc.add(spacer(4));
            }
            doc.add(spacer(8));
        }

        // Sector leaders
        if (bm.getSectorLeaders() != null && !bm.getSectorLeaders().isEmpty()) {
            doc.add(new Paragraph("Leaders du Secteur")
                .setFont(bold).setFontSize(11).setFontColor(DARK).setMarginBottom(6));
            Table lTable = new Table(UnitValue.createPercentArray(new float[]{2,1,1,2,2})).useAllAvailableWidth();
            for (String h : new String[]{"Entreprise", "Pays", "Score Est.", "Pratique Clé", "Différenciateur"}) {
                lTable.addHeaderCell(new Cell().setBackgroundColor(DARK).setPadding(6)
                    .add(new Paragraph(h).setFont(bold).setFontSize(9).setFontColor(ColorConstants.WHITE)));
            }
            boolean alt = false;
            for (BenchmarkResponse.SectorLeader l : bm.getSectorLeaders()) {
                DeviceRgb rowBg = alt ? LIGHT_BG : new DeviceRgb(255,255,255);
                lTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6)
                    .add(new Paragraph(l.getCompany() != null ? l.getCompany() : "").setFont(bold).setFontSize(9).setFontColor(DARK)));
                lTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6)
                    .add(new Paragraph(l.getCountry() != null ? l.getCountry() : "").setFont(regular).setFontSize(9)));
                lTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6).setTextAlignment(TextAlignment.CENTER)
                    .add(new Paragraph((l.getEstimatedScore() != null ? l.getEstimatedScore() : 0) + "/100")
                        .setFont(bold).setFontSize(9).setFontColor(SUCCESS)));
                lTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6)
                    .add(new Paragraph(l.getKeyPractice() != null ? l.getKeyPractice() : "").setFont(regular).setFontSize(8)));
                lTable.addCell(new Cell().setBackgroundColor(rowBg).setPadding(6)
                    .add(new Paragraph(l.getDifferentiator() != null ? l.getDifferentiator() : "").setFont(italic).setFontSize(8).setFontColor(GRAY)));
                alt = !alt;
            }
            doc.add(lTable);
            doc.add(spacer(12));
        }

        // Improvement roadmap
        if (bm.getImprovementRoadmap() != null && !bm.getImprovementRoadmap().isEmpty()) {
            doc.add(new Paragraph("Feuille de Route d'Amélioration")
                .setFont(bold).setFontSize(11).setFontColor(DARK).setMarginBottom(6));
            DeviceRgb[] phaseColors = {DANGER, PRIMARY, SUCCESS};
            int idx = 0;
            for (BenchmarkResponse.RoadmapPhase phase : bm.getImprovementRoadmap()) {
                DeviceRgb color = phaseColors[idx % phaseColors.length];
                Table pTable = new Table(UnitValue.createPercentArray(new float[]{1})).useAllAvailableWidth();
                Cell pCell = new Cell().setBorder(Border.NO_BORDER).setBorderLeft(new SolidBorder(color, 5)).setPadding(12).setMarginBottom(8);
                pCell.add(new Paragraph()
                    .add(new Text((phase.getPhase() != null ? phase.getPhase() : "") + " : ").setFont(bold).setFontSize(11).setFontColor(color))
                    .add(new Text(phase.getObjective() != null ? phase.getObjective() : "").setFont(bold).setFontSize(11).setFontColor(DARK)));
                String meta = "Investissement : " + (phase.getInvestmentLevel() != null ? phase.getInvestmentLevel() : "")
                    + "  |  Gain attendu : " + (phase.getExpectedScoreGain() != null ? phase.getExpectedScoreGain() : "")
                    + "  →  Niveau cible : " + (phase.getTargetLevel() != null ? phase.getTargetLevel() : "");
                pCell.add(new Paragraph(meta).setFont(italic).setFontSize(9).setFontColor(GRAY).setMarginTop(4).setMarginBottom(6));
                if (phase.getActions() != null) {
                    for (String action : phase.getActions()) {
                        pCell.add(new Paragraph("• " + action).setFont(regular).setFontSize(9).setFontColor(DARK).setMarginLeft(10));
                    }
                }
                pTable.addCell(pCell);
                doc.add(pTable);
                doc.add(spacer(4));
                idx++;
            }
            doc.add(spacer(8));
        }

        // Key insights
        if (bm.getKeyInsights() != null && !bm.getKeyInsights().isEmpty()) {
            doc.add(new Paragraph("Points Clés")
                .setFont(bold).setFontSize(11).setFontColor(DARK).setMarginBottom(6));
            for (String insight : bm.getKeyInsights()) {
                doc.add(new Paragraph("→ " + insight)
                    .setFont(regular).setFontSize(10).setFontColor(DARK).setMarginLeft(10).setMarginBottom(4));
            }
        }
    }

    private java.util.List<com.iabenchmark.dto.RecommendationResponse> getRecommendations(Long evaluationId) {
        if (aiService.isAiServiceAvailable()) {
            try { return aiService.getAiRecommendations(evaluationId); } catch (Exception ignored) {}
        }
        return recommendationService.generateRecommendations(evaluationId);
    }

    private Paragraph spacer(float height) {
        return new Paragraph("").setMarginBottom(height).setFontSize(1);
    }

    private Paragraph sectionTitle(String text, PdfFont bold) {
        return new Paragraph(text).setFont(bold).setFontSize(14).setFontColor(DARK)
                .setBorderBottom(new SolidBorder(PRIMARY, 2)).setPaddingBottom(4).setMarginBottom(10);
    }

    private Cell scoreCell(String label, String value, DeviceRgb color, PdfFont bold, PdfFont regular) {
        Cell cell = new Cell().setBackgroundColor(LIGHT_BG).setBorder(new SolidBorder(BORDER, 1))
                .setPadding(12).setTextAlignment(TextAlignment.CENTER).setMargin(3);
        cell.add(new Paragraph(label).setFont(regular).setFontSize(9).setFontColor(GRAY));
        cell.add(new Paragraph(value).setFont(bold).setFontSize(16).setFontColor(color));
        return cell;
    }

    private String fmt(Double v) { return v == null ? "0" : String.valueOf(Math.round(v)); }

    private String axisLabel(String axis) {
        return switch (axis) { case "BUSINESS" -> "MÉTIER"; case "PROCESS" -> "PROCESSUS"; default -> "SI"; };
    }

    private String buildAxisSummaryText(String axis, double score) {
        String level = score < 20 ? "Initial" : score < 40 ? "Basique" : score < 60 ? "Intermédiaire" : score < 80 ? "Avancé" : "Optimisé";
        return "Niveau " + level + " (" + fmt(score) + "/100). " +
               (score < 40 ? "Des lacunes importantes nécessitent des actions prioritaires." :
                score < 60 ? "Des bases solides existent. Des améliorations ciblées sont recommandées." :
                score < 80 ? "Bonne maturité. Continuer l'optimisation pour atteindre l'excellence." :
                "Excellence atteinte. Maintenir l'avance et partager les bonnes pratiques.");
    }

    private DeviceRgb maturityColor(String level) {
        return switch (level) {
            case "OPTIMISE" -> new DeviceRgb(124, 58, 237);
            case "AVANCE"   -> new DeviceRgb(5, 150, 105);
            case "INTERMEDIAIRE" -> new DeviceRgb(37, 99, 235);
            case "BASIQUE"  -> new DeviceRgb(217, 119, 6);
            default         -> new DeviceRgb(220, 38, 38);
        };
    }

    private DeviceRgb maturityBg(String level) {
        return switch (level) {
            case "OPTIMISE" -> new DeviceRgb(237, 233, 254);
            case "AVANCE"   -> new DeviceRgb(209, 250, 229);
            case "INTERMEDIAIRE" -> new DeviceRgb(219, 234, 254);
            case "BASIQUE"  -> new DeviceRgb(254, 243, 199);
            default         -> new DeviceRgb(254, 226, 226);
        };
    }
}
