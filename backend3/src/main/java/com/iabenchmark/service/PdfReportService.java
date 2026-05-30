package com.iabenchmark.service;

import com.iabenchmark.dto.BenchmarkResponse;
import com.iabenchmark.dto.EvaluationResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
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
import com.itextpdf.layout.element.AreaBreak;
import com.itextpdf.layout.element.Cell;
import com.itextpdf.layout.element.Div;
import com.itextpdf.layout.element.Paragraph;
import com.itextpdf.layout.element.Table;
import com.itextpdf.layout.element.Text;
import com.itextpdf.layout.properties.AreaBreakType;
import com.itextpdf.layout.properties.BorderRadius;
import com.itextpdf.layout.properties.TextAlignment;
import com.itextpdf.layout.properties.UnitValue;
import com.itextpdf.layout.properties.VerticalAlignment;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Locale;
import java.util.Objects;

@Service
public class PdfReportService {

    private final EvaluationRepository evaluationRepository;
    private final EvaluationService evaluationService;
    private final AiService aiService;

    // ── Couleurs (cohérentes avec l'UI Angular) ───────────────────────────────
    private static final DeviceRgb C_BLUE       = new DeviceRgb(23,  104, 229);
    private static final DeviceRgb C_DARK_BLUE  = new DeviceRgb(15,   61, 130);
    private static final DeviceRgb C_LIGHT_BLUE = new DeviceRgb(232, 240, 254);
    private static final DeviceRgb C_GREEN_DK   = new DeviceRgb(22,  101,  52);
    private static final DeviceRgb C_GREEN_LT   = new DeviceRgb(220, 252, 231);
    private static final DeviceRgb C_RED        = new DeviceRgb(220,  38,  38);
    private static final DeviceRgb C_RED_LT     = new DeviceRgb(254, 226, 226);
    private static final DeviceRgb C_ORANGE     = new DeviceRgb(217, 119,   6);
    private static final DeviceRgb C_ORANGE_LT  = new DeviceRgb(255, 237, 213);
    private static final DeviceRgb C_GRAY       = new DeviceRgb(107, 114, 128);
    private static final DeviceRgb C_LGRAY      = new DeviceRgb(249, 250, 251);
    private static final DeviceRgb C_MGRAY      = new DeviceRgb(229, 231, 235);
    private static final DeviceRgb C_TEXT       = new DeviceRgb( 31,  41,  55);

    // Couleurs par axe
    private static final DeviceRgb AX_METIER    = new DeviceRgb( 13, 110, 253);
    private static final DeviceRgb AX_PROCESS   = new DeviceRgb( 25, 135,  84);
    private static final DeviceRgb AX_SI        = new DeviceRgb( 99, 102, 241);
    private static final DeviceRgb AX_CANAUX    = new DeviceRgb(  8, 145, 178);
    private static final DeviceRgb AX_MARKETING = new DeviceRgb(217, 119,   6);
    private static final DeviceRgb AX_RH        = new DeviceRgb(124,  58, 237);
    private static final DeviceRgb AX_OFFRES    = new DeviceRgb(  5, 150, 105);

    private record AxisEntry(String label, double score, DeviceRgb color) {}

    public PdfReportService(EvaluationRepository evaluationRepository,
                            EvaluationService evaluationService,
                            AiService aiService) {
        this.evaluationRepository = evaluationRepository;
        this.evaluationService = evaluationService;
        this.aiService = aiService;
    }

    // ── Point d'entrée ────────────────────────────────────────────────────────

    public byte[] generateReport(Long evaluationId) {
        Evaluation evaluation = evaluationRepository.findById(Objects.requireNonNull(evaluationId))
                .orElseThrow(() -> new EntityNotFoundException("Evaluation not found: " + evaluationId));

        EvaluationResponse ev         = evaluationService.getEvaluation(evaluationId);
        List<RecommendationResponse> recs = aiService.getStoredRecommendations(evaluation);
        BenchmarkResponse benchmark   = aiService.getStoredBenchmark(evaluation);

        String sector  = evaluation.getCompany().getSector()  != null ? evaluation.getCompany().getSector()  : "-";
        String country = evaluation.getCompany().getCountry() != null ? evaluation.getCompany().getCountry() : "-";

        try (ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
            PdfWriter   writer = new PdfWriter(baos);
            PdfDocument pdf    = new PdfDocument(writer);
            Document    doc    = new Document(pdf, PageSize.A4);
            doc.setMargins(50, 45, 50, 45);

            PdfFont regular = PdfFontFactory.createFont(StandardFonts.HELVETICA,      "Cp1252");
            PdfFont bold    = PdfFontFactory.createFont(StandardFonts.HELVETICA_BOLD, "Cp1252");

            addCoverPage(doc, ev, sector, country, regular, bold);

            doc.add(new AreaBreak(AreaBreakType.NEXT_PAGE));
            addScoresSection(doc, ev, regular, bold);

            if (!recs.isEmpty()) {
                doc.add(new AreaBreak(AreaBreakType.NEXT_PAGE));
                addRecommendationsSection(doc, recs, regular, bold);
            }

            if (benchmark != null) {
                doc.add(new AreaBreak(AreaBreakType.NEXT_PAGE));
                addBenchmarkSection(doc, benchmark, regular, bold);

                List<BenchmarkResponse.RoadmapPhase> roadmap = benchmark.getImprovementRoadmap();
                if (roadmap != null && !roadmap.isEmpty()) {
                    doc.add(new AreaBreak(AreaBreakType.NEXT_PAGE));
                    addRoadmapSection(doc, roadmap, regular, bold);
                }
            }

            doc.close();
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("Erreur generation PDF", e);
        }
    }

    // ── Page de garde ─────────────────────────────────────────────────────────

    private void addCoverPage(Document doc, EvaluationResponse ev,
                              String sector, String country,
                              PdfFont r, PdfFont b) {
        // Bande bleue en haut
        doc.add(fullColorBar(C_DARK_BLUE, 10));
        doc.add(spacer(70));

        // En-tête
        doc.add(para("IA BENCHMARK", b, 10, C_GRAY));
        doc.add(para("Rapport d'Evaluation de Maturite Digitale", b, 24, C_DARK_BLUE)
                .setMarginBottom(4));
        doc.add(hLine(C_BLUE, 3));
        doc.add(spacer(40));

        // Nom entreprise
        doc.add(para(ev.getCompanyName(), b, 30, C_BLUE).setMarginBottom(20));

        // Tableau infos
        Table info = new Table(new float[]{1, 1})
                .setWidth(UnitValue.createPercentValue(85));
        info.addCell(infoCell("Secteur d'activite", sector, r, b));
        info.addCell(infoCell("Pays", country, r, b));
        info.addCell(infoCell("Date du rapport",
                LocalDate.now().format(DateTimeFormatter.ofPattern("dd MMMM yyyy", Locale.FRENCH)), r, b));
        info.addCell(infoCell("Score global", String.format("%.1f / 100", ev.getGlobalScore()), r, b));
        doc.add(info);
        doc.add(spacer(36));

        // Badge niveau de maturite
        String      matLabel  = maturityLabel(ev.getMaturityLevel() != null ? ev.getMaturityLevel().name() : "");
        DeviceRgb[] matColors = maturityColors(ev.getMaturityLevel() != null ? ev.getMaturityLevel().name() : "");
        Table badge = new Table(new float[]{1}).setWidth(UnitValue.createPointValue(230));
        badge.addCell(new Cell()
                .add(new Paragraph("Niveau : " + matLabel)
                        .setFont(b).setFontSize(13).setFontColor(matColors[1]).setMargin(0))
                .setBackgroundColor(matColors[0])
                .setBorder(Border.NO_BORDER)
                .setPadding(12)
                .setBorderRadius(new BorderRadius(6)));
        doc.add(badge);

        if (ev.getTargetMaturityLevel() != null) {
            doc.add(spacer(10));
            String targetLabel = maturityLabel(ev.getTargetMaturityLevel().name());
            doc.add(new Paragraph()
                    .add(new Text("Maturite cible : ").setFont(r).setFontSize(11).setFontColor(C_GRAY))
                    .add(new Text(targetLabel).setFont(b).setFontSize(11).setFontColor(C_GREEN_DK))
                    .setMargin(0));
        }

        // Pied de page de garde
        doc.add(spacer(50));
        doc.add(hLine(C_MGRAY, 1));
        doc.add(spacer(12));
        doc.add(para("Ce rapport a ete genere automatiquement par la plateforme IA Benchmark. "
                + "Il synthetise les resultats de l'evaluation de maturite digitale de "
                + ev.getCompanyName() + " dans le secteur " + sector + ".", r, 9, C_GRAY));
        doc.add(spacer(30));
        doc.add(fullColorBar(C_DARK_BLUE, 8));
    }

    // ── Scores ────────────────────────────────────────────────────────────────

    private void addScoresSection(Document doc, EvaluationResponse ev, PdfFont r, PdfFont b) {
        sectionTitle(doc, "Scores de Maturite Digitale", b);

        // Carte score global + niveau
        Table scoreCard = new Table(new float[]{1, 2})
                .setWidth(UnitValue.createPercentValue(100));

        String      matLabel  = maturityLabel(ev.getMaturityLevel() != null ? ev.getMaturityLevel().name() : "");
        DeviceRgb[] matColors = maturityColors(ev.getMaturityLevel() != null ? ev.getMaturityLevel().name() : "");

        scoreCard.addCell(new Cell()
                .add(para(String.format("%.0f", ev.getGlobalScore()), b, 54, C_BLUE)
                        .setTextAlignment(TextAlignment.CENTER))
                .add(para("/ 100", r, 13, C_GRAY).setTextAlignment(TextAlignment.CENTER))
                .setVerticalAlignment(VerticalAlignment.MIDDLE)
                .setBackgroundColor(C_LGRAY)
                .setBorder(new SolidBorder(C_MGRAY, 1))
                .setPadding(20));

        Cell infoC = new Cell()
                .add(para("Niveau de maturite", r, 10, C_GRAY))
                .add(new Paragraph(matLabel)
                        .setFont(b).setFontSize(16).setFontColor(matColors[1])
                        .setBackgroundColor(matColors[0])
                        .setPaddingLeft(10).setPaddingRight(10)
                        .setPaddingTop(4).setPaddingBottom(4)
                        .setMarginTop(4).setMarginBottom(0))
                .setBorder(new SolidBorder(C_MGRAY, 1))
                .setPadding(20)
                .setVerticalAlignment(VerticalAlignment.MIDDLE);
        if (ev.getTargetMaturityLevel() != null) {
            String tl = maturityLabel(ev.getTargetMaturityLevel().name());
            infoC.add(spacer(10))
                 .add(para("Maturite cible", r, 10, C_GRAY))
                 .add(para(tl, b, 13, C_GREEN_DK).setMarginTop(2));
        }
        scoreCard.addCell(infoC);
        doc.add(scoreCard);
        doc.add(spacer(24));

        // Barres par axe
        sectionSubtitle(doc, "Scores par axe", b);
        List<AxisEntry> axes = List.of(
                new AxisEntry("Metier",                    axisScore(ev, "METIER"),                   AX_METIER),
                new AxisEntry("Processus",                 axisScore(ev, "PROCESSUS"),                AX_PROCESS),
                new AxisEntry("Systeme d'Information",     axisScore(ev, "SI"),                       AX_SI),
                new AxisEntry("Canaux & UX",               axisScore(ev, "CANAUX_DISTRIBUTION"),       AX_CANAUX),
                new AxisEntry("Marketing & Communication", axisScore(ev, "MARKETING_COMMUNICATION"),   AX_MARKETING),
                new AxisEntry("RH & Culture Digitale",     axisScore(ev, "RH_CULTURE_DIGITALE"),       AX_RH),
                new AxisEntry("Offres Digitales",          axisScore(ev, "OFFRES_DIGITALES"),          AX_OFFRES)
        );

        for (AxisEntry ax : axes) {
            if (ax.score() <= 0) continue;
            doc.add(axisBar(ax.label(), ax.score(), ax.color(), r, b));
            doc.add(spacer(6));
        }
    }

    // ── Recommandations ───────────────────────────────────────────────────────

    private void addRecommendationsSection(Document doc, List<RecommendationResponse> recs,
                                           PdfFont r, PdfFont b) {
        sectionTitle(doc, "Recommandations (" + recs.size() + ")", b);

        for (String priority : List.of("HAUTE", "MOYENNE", "BASSE")) {
            List<RecommendationResponse> group = recs.stream()
                    .filter(rc -> priority.equals(rc.getPriority())).toList();
            if (group.isEmpty()) continue;

            DeviceRgb[] pc = priorityColors(priority);

            // Sous-titre priorité
            doc.add(new Paragraph(priorityLabel(priority) + " priorite  (" + group.size() + ")")
                    .setFont(b).setFontSize(11).setFontColor(pc[1])
                    .setBackgroundColor(pc[0])
                    .setPaddingLeft(10).setPaddingRight(10)
                    .setPaddingTop(5).setPaddingBottom(5)
                    .setMarginBottom(8).setMarginTop(6));

            for (RecommendationResponse rec : group) {
                Table card = new Table(new float[]{1})
                        .setWidth(UnitValue.createPercentValue(100));
                Cell  c   = new Cell()
                        .setBorderLeft(new SolidBorder(pc[1], 4))
                        .setBorderTop(new SolidBorder(C_MGRAY, 1))
                        .setBorderRight(new SolidBorder(C_MGRAY, 1))
                        .setBorderBottom(new SolidBorder(C_MGRAY, 1))
                        .setBackgroundColor(ColorConstants.WHITE)
                        .setPadding(12);

                // Axe badge
                c.add(new Paragraph(axisLabel(rec.getAxis()))
                        .setFont(r).setFontSize(8).setFontColor(C_GRAY).setMarginBottom(4));
                // Titre
                c.add(para(rec.getTitle(), b, 11, C_TEXT));
                // Description
                if (nonBlank(rec.getDescription())) {
                    c.add(para(rec.getDescription(), r, 9, C_GRAY).setMarginTop(5));
                }
                // Best practice
                if (nonBlank(rec.getBestPractice())) {
                    c.add(new Paragraph()
                            .add(new Text("Bonne pratique : ").setFont(b).setFontSize(9).setFontColor(C_BLUE))
                            .add(new Text(rec.getBestPractice()).setFont(r).setFontSize(9).setFontColor(C_TEXT))
                            .setMarginTop(6));
                }
                // Source
                if (nonBlank(rec.getSource())) {
                    c.add(new Paragraph()
                            .add(new Text("Source : ").setFont(b).setFontSize(8).setFontColor(C_GRAY))
                            .add(new Text(rec.getSource()).setFont(r).setFontSize(8).setFontColor(C_GRAY))
                            .setMarginTop(4));
                }
                card.addCell(c);
                doc.add(card);
                doc.add(spacer(5));
            }
            doc.add(spacer(10));
        }
    }

    // ── Benchmarking ──────────────────────────────────────────────────────────

    private void addBenchmarkSection(Document doc, BenchmarkResponse bm, PdfFont r, PdfFont b) {
        sectionTitle(doc, "Benchmarking Sectoriel", b);

        // Résumé exécutif
        if (nonBlank(bm.getExecutiveSummary())) {
            doc.add(para(bm.getExecutiveSummary(), r, 10, C_TEXT)
                    .setBackgroundColor(C_LIGHT_BLUE)
                    .setPadding(12).setMarginBottom(18));
        }

        // Cartes KPI
        if (bm.getSectorBenchmark() != null) {
            BenchmarkResponse.SectorBenchmark sb = bm.getSectorBenchmark();
            Table cards = new Table(new float[]{1, 1, 1})
                    .setWidth(UnitValue.createPercentValue(100));
            cards.addCell(kpiCard("Moyenne nationale",
                    String.format("%.0f", sb.getNationalAverage()), C_BLUE, r, b));
            cards.addCell(kpiCard("Moyenne internationale",
                    String.format("%.0f", sb.getInternationalAverage()), C_GREEN_DK, r, b));
            cards.addCell(kpiCard("Positionnement",
                    sb.getPositioningLabel() + "\nPercentile " + sb.getCompanyPercentile() + "e",
                    C_BLUE, r, b));
            doc.add(cards);
            doc.add(spacer(18));
        }

        // Tableau comparaison par axe
        if (bm.getAxisBenchmarks() != null && !bm.getAxisBenchmarks().isEmpty()) {
            sectionSubtitle(doc, "Comparaison par axe", b);
            Table t = new Table(new float[]{3f, 1.4f, 1.6f, 1.4f, 1.4f})
                    .setWidth(UnitValue.createPercentValue(100));

            for (String h : List.of("Axe", "Votre score", "Moy. sectorielle", "Top quartile", "Ecart")) {
                t.addHeaderCell(new Cell()
                        .add(para(h, b, 9, new DeviceRgb(255, 255, 255)))
                        .setBackgroundColor(C_DARK_BLUE)
                        .setBorder(Border.NO_BORDER)
                        .setPadding(8));
            }

            boolean alt = false;
            for (BenchmarkResponse.AxisBenchmark ab : bm.getAxisBenchmarks()) {
                DeviceRgb bg      = alt ? C_LGRAY : new DeviceRgb(255, 255, 255);
                alt = !alt;
                double    gap     = ab.getGapToAverage() != null ? ab.getGapToAverage() : 0;
                DeviceRgb gapCol  = gap >= 0 ? C_GREEN_DK : C_RED;
                String    gapStr  = (gap >= 0 ? "+" : "") + String.format("%.1f", gap);

                t.addCell(tCell(ab.getAxisLabel() != null ? ab.getAxisLabel() : ab.getAxis(),
                        r, 9, C_TEXT, bg, TextAlignment.LEFT));
                t.addCell(tCell(String.format("%.1f", ab.getCompanyScore()),
                        b, 9, C_BLUE, bg, TextAlignment.CENTER));
                t.addCell(tCell(String.format("%.1f", ab.getSectorAverage()),
                        r, 9, C_TEXT, bg, TextAlignment.CENTER));
                t.addCell(tCell(String.format("%.1f", ab.getTopQuartile()),
                        r, 9, C_TEXT, bg, TextAlignment.CENTER));
                t.addCell(tCell(gapStr, b, 9, gapCol, bg, TextAlignment.CENTER));
            }
            doc.add(t);
            doc.add(spacer(18));
        }

        // Leaders sectoriels
        if (bm.getSectorLeaders() != null && !bm.getSectorLeaders().isEmpty()) {
            sectionSubtitle(doc, "Leaders sectoriels de reference", b);
            Table lt = new Table(new float[]{2f, 1f, 1f, 4f})
                    .setWidth(UnitValue.createPercentValue(100));
            for (String h : List.of("Entreprise", "Pays", "Score", "Pratique cle")) {
                lt.addHeaderCell(new Cell()
                        .add(para(h, b, 9, new DeviceRgb(255, 255, 255)))
                        .setBackgroundColor(C_DARK_BLUE)
                        .setBorder(Border.NO_BORDER).setPadding(8));
            }
            boolean alt = false;
            for (BenchmarkResponse.SectorLeader l : bm.getSectorLeaders()) {
                DeviceRgb bg = alt ? C_LGRAY : new DeviceRgb(255, 255, 255);
                alt = !alt;
                lt.addCell(tCell(l.getCompany(), b, 9, C_TEXT, bg, TextAlignment.LEFT));
                lt.addCell(tCell(l.getCountry(), r, 9, C_GRAY, bg, TextAlignment.LEFT));
                lt.addCell(tCell(l.getEstimatedScore() != null ? l.getEstimatedScore().toString() : "-",
                        b, 9, C_BLUE, bg, TextAlignment.CENTER));
                lt.addCell(tCell(l.getKeyPractice(), r, 9, C_TEXT, bg, TextAlignment.LEFT));
            }
            doc.add(lt);
            doc.add(spacer(18));
        }

        // Tendances
        if (bm.getTrends() != null && !bm.getTrends().isEmpty()) {
            sectionSubtitle(doc, "Tendances sectorielles", b);
            for (BenchmarkResponse.BenchmarkTrend t : bm.getTrends()) {
                Table card = new Table(new float[]{1})
                        .setWidth(UnitValue.createPercentValue(100));
                Cell  c   = new Cell()
                        .setBorder(new SolidBorder(C_MGRAY, 1))
                        .setBackgroundColor(C_LGRAY)
                        .setPadding(10).setMarginBottom(6);

                DeviceRgb[] ic = impactColors(t.getImpactLevel() != null ? t.getImpactLevel() : "MOYEN");
                c.add(new Paragraph()
                        .add(new Text(t.getTitle()).setFont(b).setFontSize(10).setFontColor(C_TEXT))
                        .add(new Text("  " + (t.getImpactLevel() != null ? t.getImpactLevel() : ""))
                                .setFont(b).setFontSize(8).setFontColor(ic[1]).setBackgroundColor(ic[0])));
                if (nonBlank(t.getDescription())) {
                    c.add(para(t.getDescription(), r, 9, C_GRAY).setMarginTop(4));
                }
                if (nonBlank(t.getHorizon())) {
                    c.add(new Paragraph()
                            .add(new Text(t.getHorizon() + "  ·  Adoption : "
                                    + (nonBlank(t.getAdoptionRate()) ? t.getAdoptionRate() : "-"))
                                    .setFont(r).setFontSize(8).setFontColor(C_GRAY)));
                }
                if (nonBlank(t.getSource())) {
                    c.add(new Paragraph()
                            .add(new Text("Source : ").setFont(b).setFontSize(8).setFontColor(C_BLUE))
                            .add(new Text(t.getSource()).setFont(r).setFontSize(8).setFontColor(C_BLUE)));
                }
                card.addCell(c);
                doc.add(card);
            }
        }
    }

    // ── Feuille de route ──────────────────────────────────────────────────────

    private void addRoadmapSection(Document doc, List<BenchmarkResponse.RoadmapPhase> roadmap,
                                   PdfFont r, PdfFont b) {
        sectionTitle(doc, "Feuille de Route d'Amelioration", b);

        DeviceRgb[] phaseColors = {C_BLUE, C_GREEN_DK, new DeviceRgb(124, 58, 237)};

        for (int i = 0; i < roadmap.size(); i++) {
            BenchmarkResponse.RoadmapPhase p  = roadmap.get(i);
            DeviceRgb                      pc = phaseColors[Math.min(i, phaseColors.length - 1)];

            Table card = new Table(new float[]{1}).setWidth(UnitValue.createPercentValue(100));
            Cell  c   = new Cell()
                    .setBorderLeft(new SolidBorder(pc, 5))
                    .setBorderTop(new SolidBorder(C_MGRAY, 1))
                    .setBorderRight(new SolidBorder(C_MGRAY, 1))
                    .setBorderBottom(new SolidBorder(C_MGRAY, 1))
                    .setBackgroundColor(C_LGRAY)
                    .setPadding(14);

            c.add(para(p.getPhase(), b, 12, pc));
            if (nonBlank(p.getObjective())) {
                c.add(para(p.getObjective(), r, 10, C_TEXT).setMarginTop(4));
            }
            if (p.getActions() != null && !p.getActions().isEmpty()) {
                c.add(spacer(6));
                for (String action : p.getActions()) {
                    c.add(new Paragraph()
                            .add(new Text("  •  ").setFont(b).setFontSize(9).setFontColor(pc))
                            .add(new Text(action).setFont(r).setFontSize(9).setFontColor(C_TEXT))
                            .setMarginBottom(2));
                }
            }
            if (nonBlank(p.getExpectedScoreGain()) || nonBlank(p.getInvestmentLevel())) {
                c.add(spacer(8));
                Paragraph meta = new Paragraph().setMargin(0);
                if (nonBlank(p.getExpectedScoreGain())) {
                    meta.add(new Text("Gain attendu : " + p.getExpectedScoreGain() + "   ")
                            .setFont(b).setFontSize(9).setFontColor(C_GREEN_DK));
                }
                if (nonBlank(p.getInvestmentLevel())) {
                    meta.add(new Text("Investissement : " + p.getInvestmentLevel())
                            .setFont(r).setFontSize(9).setFontColor(C_GRAY));
                }
                c.add(meta);
            }
            card.addCell(c);
            doc.add(card);
            doc.add(spacer(10));
        }
    }

    // ── Helpers visuels ───────────────────────────────────────────────────────

    private Div axisBar(String label, double score, DeviceRgb color, PdfFont r, PdfFont b) {
        Div d = new Div().setWidth(UnitValue.createPercentValue(100));

        Table labelRow = new Table(new float[]{5, 1}).setWidth(UnitValue.createPercentValue(100));
        labelRow.addCell(new Cell().add(para(label, b, 9, C_TEXT))
                .setBorder(Border.NO_BORDER).setPadding(0).setPaddingBottom(2));
        labelRow.addCell(new Cell().add(para(String.format("%.1f/100", score), r, 9, C_GRAY)
                        .setTextAlignment(TextAlignment.RIGHT))
                .setBorder(Border.NO_BORDER).setPadding(0).setPaddingBottom(2));
        d.add(labelRow);

        float filled = (float) Math.max(1, Math.min(99, score));
        float empty  = 100f - filled;
        Table bar = new Table(new float[]{filled, empty})
                .setWidth(UnitValue.createPercentValue(100)).setHeight(10);
        bar.addCell(new Cell().setBackgroundColor(color)
                .setBorder(Border.NO_BORDER).setPadding(0));
        bar.addCell(new Cell().setBackgroundColor(C_MGRAY)
                .setBorder(Border.NO_BORDER).setPadding(0));
        d.add(bar);
        return d;
    }

    private Cell kpiCard(String title, String value, DeviceRgb valColor, PdfFont r, PdfFont b) {
        return new Cell()
                .add(para(title, r, 9, C_GRAY).setTextAlignment(TextAlignment.CENTER))
                .add(para(value, b, 13, valColor).setTextAlignment(TextAlignment.CENTER).setMarginTop(4))
                .setBackgroundColor(C_LGRAY)
                .setBorder(new SolidBorder(C_MGRAY, 1))
                .setPadding(12)
                .setBorderRadius(new BorderRadius(6));
    }

    private Table fullColorBar(DeviceRgb color, float height) {
        Table t = new Table(new float[]{1}).setWidth(UnitValue.createPercentValue(100));
        t.addCell(new Cell().setBackgroundColor(color)
                .setBorder(Border.NO_BORDER).setPadding(0).setHeight(height));
        return t;
    }

    private void sectionTitle(Document doc, String text, PdfFont b) {
        doc.add(new Paragraph(text)
                .setFont(b).setFontSize(18).setFontColor(C_DARK_BLUE)
                .setBorderBottom(new SolidBorder(C_BLUE, 2))
                .setMarginBottom(16).setPaddingBottom(6));
    }

    private void sectionSubtitle(Document doc, String text, PdfFont b) {
        doc.add(para(text, b, 12, C_TEXT).setMarginTop(12).setMarginBottom(8));
    }

    private Table hLine(DeviceRgb color, float width) {
        Table t = new Table(new float[]{1}).setWidth(UnitValue.createPercentValue(100));
        t.addCell(new Cell().setBorder(Border.NO_BORDER)
                .setBorderBottom(new SolidBorder(color, width)).setPadding(0).setHeight(1));
        return t;
    }

    private Paragraph para(String text, PdfFont font, float size, DeviceRgb color) {
        return new Paragraph(text != null ? text : "")
                .setFont(font).setFontSize(size).setFontColor(color).setMargin(0);
    }

    private Div spacer(float h) { return new Div().setHeight(h); }

    private Cell infoCell(String label, String value, PdfFont r, PdfFont b) {
        return new Cell()
                .add(para(label, r, 9, C_GRAY))
                .add(para(value,  b, 11, C_TEXT))
                .setBorder(Border.NO_BORDER)
                .setBorderBottom(new SolidBorder(C_MGRAY, 1))
                .setPadding(10);
    }

    private Cell tCell(String text, PdfFont font, float size, DeviceRgb color,
                       DeviceRgb bg, TextAlignment align) {
        return new Cell()
                .add(new Paragraph(text != null ? text : "")
                        .setFont(font).setFontSize(size).setFontColor(color)
                        .setMargin(0).setTextAlignment(align))
                .setBackgroundColor(bg)
                .setBorder(new SolidBorder(C_MGRAY, 0.5f))
                .setPadding(7);
    }

    // ── Utilitaires métier ────────────────────────────────────────────────────

    private double axisScore(EvaluationResponse ev, String axisKey) {
        if (ev.getScoresByAxis() == null) return 0;
        return ev.getScoresByAxis().stream()
                .filter(a -> axisKey.equalsIgnoreCase(a.getAxis()))
                .findFirst().map(a -> a.getScore() != null ? a.getScore() : 0.0).orElse(0.0);
    }

    private boolean nonBlank(String s) { return s != null && !s.isBlank(); }

    private String maturityLabel(String level) {
        if (level == null) return "";
        return switch (level) {
            case "INITIAL"       -> "Initial";
            case "BASIQUE"       -> "Basique";
            case "INTERMEDIAIRE" -> "Intermediaire";
            case "AVANCE"        -> "Avance";
            case "OPTIMISE"      -> "Optimise";
            default              -> level;
        };
    }

    private DeviceRgb[] maturityColors(String level) {
        if (level == null) return new DeviceRgb[]{C_LGRAY, C_GRAY};
        return switch (level) {
            case "INITIAL"       -> new DeviceRgb[]{C_RED_LT,    C_RED};
            case "BASIQUE"       -> new DeviceRgb[]{C_ORANGE_LT,  C_ORANGE};
            case "INTERMEDIAIRE" -> new DeviceRgb[]{C_LIGHT_BLUE, C_BLUE};
            case "AVANCE"        -> new DeviceRgb[]{C_GREEN_LT,   C_GREEN_DK};
            case "OPTIMISE"      -> new DeviceRgb[]{C_GREEN_LT,   C_GREEN_DK};
            default              -> new DeviceRgb[]{C_LGRAY,      C_GRAY};
        };
    }

    private DeviceRgb[] priorityColors(String priority) {
        return switch (priority) {
            case "HAUTE" -> new DeviceRgb[]{C_RED_LT,   C_RED};
            case "BASSE" -> new DeviceRgb[]{C_GREEN_LT,  C_GREEN_DK};
            default      -> new DeviceRgb[]{C_ORANGE_LT, C_ORANGE};
        };
    }

    private DeviceRgb[] impactColors(String level) {
        return switch (level.toUpperCase()) {
            case "ELEVE", "ELEVÉ", "HIGH" -> new DeviceRgb[]{C_ORANGE_LT, C_ORANGE};
            case "FAIBLE", "LOW"               -> new DeviceRgb[]{C_GREEN_LT,  C_GREEN_DK};
            default                            -> new DeviceRgb[]{C_LIGHT_BLUE, C_BLUE};
        };
    }

    private String priorityLabel(String priority) {
        return switch (priority) {
            case "HAUTE" -> "Haute";
            case "BASSE" -> "Basse";
            default      -> "Moyenne";
        };
    }

    private String axisLabel(String axis) {
        if (axis == null) return "";
        return switch (axis) {
            case "METIER"    -> "Metier";
            case "PROCESSUS" -> "Processus";
            case "SI"        -> "Systeme d'Information";
            case "CANAUX"    -> "Canaux & UX";
            case "MARKETING" -> "Marketing & Communication";
            case "RH"        -> "RH & Culture Digitale";
            case "OFFRES"    -> "Offres Digitales";
            default          -> axis;
        };
    }
}
