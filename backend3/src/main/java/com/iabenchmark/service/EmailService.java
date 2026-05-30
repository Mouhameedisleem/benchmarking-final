package com.iabenchmark.service;

import com.iabenchmark.dto.BenchmarkResponse;
import com.iabenchmark.dto.RecommendationResponse;
import com.iabenchmark.model.Evaluation;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import org.springframework.core.io.ByteArrayResource;
import java.util.List;
import java.util.Objects;

@Service
public class EmailService {

    private final JavaMailSender mailSender;

    @Value("${app.mail.from}")
    private String fromAddress;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void sendCompanyCredentials(String toEmail, String companyName, String login, String password) {
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            helper.setFrom(Objects.requireNonNull(fromAddress));
            helper.setTo(Objects.requireNonNull(toEmail));
            helper.setSubject("Vos accès à la plateforme IA Benchmark — " + companyName);

            String html = """
                <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:520px;margin:0 auto;background:#f8faff;border-radius:16px;overflow:hidden;">
                  <div style="background:linear-gradient(135deg,#0f2242 0%%,#1768e5 100%%);padding:36px 40px;text-align:center;">
                    <h1 style="color:#fff;margin:0;font-size:26px;font-weight:800;">IA Benchmark</h1>
                    <p style="color:rgba(255,255,255,0.75);margin:8px 0 0;font-size:14px;">Plateforme d'évaluation de maturité digitale</p>
                  </div>
                  <div style="padding:40px;">
                    <h2 style="color:#0f2242;font-size:20px;margin:0 0 12px;">Bienvenue, %s !</h2>
                    <p style="color:#4b5563;line-height:1.7;margin:0 0 24px;">
                      Un consultant vous a inscrit sur la plateforme IA Benchmark. Voici vos identifiants de connexion :
                    </p>
                    <div style="background:#fff;border:2px solid #e8f0fe;border-radius:12px;padding:24px;margin-bottom:28px;">
                      <table style="width:100%%;border-collapse:collapse;">
                        <tr><td style="color:#6b7280;font-size:13px;padding:6px 0;font-weight:600;">Identifiant (email)</td>
                            <td style="color:#1768e5;font-size:14px;padding:6px 0;font-weight:700;">%s</td></tr>
                        <tr><td style="color:#6b7280;font-size:13px;padding:6px 0;font-weight:600;">Mot de passe</td>
                            <td style="color:#1768e5;font-size:14px;padding:6px 0;font-weight:700;">%s</td></tr>
                      </table>
                    </div>
                    <p style="color:#4b5563;line-height:1.7;margin:0 0 24px;">
                      Connectez-vous sur <a href="http://localhost:4200/login" style="color:#1768e5;">la plateforme</a>
                      pour répondre à votre questionnaire de maturité digitale.
                    </p>
                    <p style="color:#9ca3af;font-size:13px;">Nous vous recommandons de changer votre mot de passe après la première connexion.</p>
                  </div>
                  <div style="background:#f1f5f9;padding:20px 40px;text-align:center;">
                    <p style="color:#9ca3af;font-size:12px;margin:0;">© 2025 IA Benchmark — Ne pas répondre à cet email</p>
                  </div>
                </div>
                """.formatted(companyName, login, password);

            helper.setText(Objects.requireNonNull(html), true);
            mailSender.send(message);
        } catch (MessagingException e) {
            throw new RuntimeException("Échec de l'envoi de l'email : " + e.getMessage(), e);
        }
    }

    public void sendEvaluationResults(String toEmail, String companyName,
                                      Evaluation evaluation,
                                      List<RecommendationResponse> recommendations,
                                      BenchmarkResponse benchmark,
                                      Long evaluationId,
                                      byte[] pdfBytes) {
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            helper.setFrom(Objects.requireNonNull(fromAddress));
            helper.setTo(Objects.requireNonNull(toEmail));
            helper.setSubject("Vos résultats d'évaluation de maturité digitale — " + companyName);

            String maturity = evaluation.getMaturityLevel() != null ? evaluation.getMaturityLevel().name() : "—";
            String globalScore = String.format("%.1f", evaluation.getGlobalScore());

            // ── 7 axes scores ───────────────────────────────────────────────────
            String[][] axisData = {
                {"Axe Métier",                      String.format("%.1f", evaluation.getBusinessScore())},
                {"Axe Processus",                   String.format("%.1f", evaluation.getProcessScore())},
                {"Axe Système d'Information",       String.format("%.1f", evaluation.getInformationSystemScore())},
                {"Axe Canaux & Distribution",       String.format("%.1f", evaluation.getCanauxDistributionScore())},
                {"Axe Marketing & Communication",   String.format("%.1f", evaluation.getMarketingCommunicationScore())},
                {"Axe RH & Culture Digitale",       String.format("%.1f", evaluation.getRhCultureDigitaleScore())},
                {"Axe Offres Digitales",            String.format("%.1f", evaluation.getOffresDigitalesScore())}
            };
            StringBuilder axesHtml = new StringBuilder();
            for (int i = 0; i < axisData.length; i++) {
                String border = i == 0 ? "" : "border-top:1px solid #f1f5f9;";
                axesHtml.append("<tr style=\"").append(border).append("\">")
                    .append("<td style=\"padding:8px 0;color:#6b7280;font-size:13px;\">").append(axisData[i][0]).append("</td>")
                    .append("<td style=\"padding:8px 0;font-weight:700;color:#0f2242;text-align:right;\">").append(axisData[i][1]).append("/100</td>")
                    .append("</tr>");
            }

            // ── Recommendations ─────────────────────────────────────────────────
            StringBuilder recsHtml = new StringBuilder();
            if (recommendations != null && !recommendations.isEmpty()) {
                for (RecommendationResponse rec : recommendations) {
                    String badgeColor = "HAUTE".equals(rec.getPriority()) ? "#dc2626"
                            : "MOYENNE".equals(rec.getPriority()) ? "#d97706" : "#16a34a";
                    recsHtml.append("<div style=\"border-left:4px solid ").append(badgeColor)
                        .append(";padding:12px 16px;margin-bottom:12px;background:#fff;border-radius:0 8px 8px 0;\">")
                        .append("<div style=\"display:flex;align-items:center;gap:8px;margin-bottom:6px;\">")
                        .append("<span style=\"background:").append(badgeColor).append(";color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;\">").append(rec.getPriority()).append("</span>")
                        .append("<span style=\"font-weight:700;color:#0f2242;font-size:14px;\">").append(rec.getTitle()).append("</span>")
                        .append("</div>")
                        .append("<p style=\"color:#4b5563;font-size:13px;margin:0 0 6px;\">").append(rec.getDescription()).append("</p>")
                        .append("<p style=\"color:#6b7280;font-size:12px;margin:0;font-style:italic;\">").append(rec.getBestPractice()).append("</p>")
                        .append("</div>");
                }
            } else {
                recsHtml.append("<p style=\"color:#6b7280;font-size:13px;\">Aucune recommandation disponible.</p>");
            }

            // ── Sector benchmark summary ────────────────────────────────────────
            String nationalAvg  = benchmark != null && benchmark.getSectorBenchmark() != null
                    && benchmark.getSectorBenchmark().getNationalAverage() != null
                    ? String.format("%.1f", benchmark.getSectorBenchmark().getNationalAverage()) : "—";
            String intlAvg      = benchmark != null && benchmark.getSectorBenchmark() != null
                    && benchmark.getSectorBenchmark().getInternationalAverage() != null
                    ? String.format("%.1f", benchmark.getSectorBenchmark().getInternationalAverage()) : "—";
            String topQuartile  = benchmark != null && benchmark.getSectorBenchmark() != null
                    && benchmark.getSectorBenchmark().getTopQuartileScore() != null
                    ? String.format("%.1f", benchmark.getSectorBenchmark().getTopQuartileScore()) : "—";
            String positioning  = benchmark != null && benchmark.getSectorBenchmark() != null
                    && benchmark.getSectorBenchmark().getPositioningLabel() != null
                    ? benchmark.getSectorBenchmark().getPositioningLabel() : "—";
            String percentile   = benchmark != null && benchmark.getSectorBenchmark() != null
                    && benchmark.getSectorBenchmark().getCompanyPercentile() != null
                    ? benchmark.getSectorBenchmark().getCompanyPercentile() + "e percentile" : "—";

            // ── Axis benchmark comparison table ─────────────────────────────────
            StringBuilder axisBenchHtml = new StringBuilder();
            if (benchmark != null && benchmark.getAxisBenchmarks() != null && !benchmark.getAxisBenchmarks().isEmpty()) {
                axisBenchHtml.append("<h4 style=\"color:#0f2242;font-size:14px;margin:20px 0 10px;font-weight:700;\">Comparaison par axe</h4>")
                    .append("<table style=\"width:100%;border-collapse:collapse;font-size:12px;\">")
                    .append("<thead><tr style=\"background:#f1f5f9;\">")
                    .append("<th style=\"padding:8px;text-align:left;color:#4b5563;font-weight:600;\">Axe</th>")
                    .append("<th style=\"padding:8px;text-align:center;color:#4b5563;font-weight:600;\">Votre score</th>")
                    .append("<th style=\"padding:8px;text-align:center;color:#4b5563;font-weight:600;\">Moy. secteur</th>")
                    .append("<th style=\"padding:8px;text-align:center;color:#4b5563;font-weight:600;\">Top quartile</th>")
                    .append("<th style=\"padding:8px;text-align:center;color:#4b5563;font-weight:600;\">Écart moy.</th>")
                    .append("</tr></thead><tbody>");
                boolean firstRow = true;
                for (BenchmarkResponse.AxisBenchmark ab : benchmark.getAxisBenchmarks()) {
                    String rowBorder = firstRow ? "" : "border-top:1px solid #f1f5f9;";
                    String gapColor  = ab.getGapToAverage() != null && ab.getGapToAverage() >= 0 ? "#16a34a" : "#dc2626";
                    String gapStr    = ab.getGapToAverage() != null
                            ? (ab.getGapToAverage() >= 0 ? "+" : "") + String.format("%.1f", ab.getGapToAverage()) : "—";
                    String axLabel   = ab.getAxisLabel() != null ? ab.getAxisLabel() : (ab.getAxis() != null ? ab.getAxis() : "—");
                    String coScore   = ab.getCompanyScore()  != null ? String.format("%.1f", ab.getCompanyScore())  : "—";
                    String secAvg    = ab.getSectorAverage() != null ? String.format("%.1f", ab.getSectorAverage()) : "—";
                    String topQ      = ab.getTopQuartile()   != null ? String.format("%.1f", ab.getTopQuartile())   : "—";
                    axisBenchHtml.append("<tr style=\"").append(rowBorder).append("\">")
                        .append("<td style=\"padding:8px;color:#0f2242;font-weight:600;\">").append(axLabel).append("</td>")
                        .append("<td style=\"padding:8px;text-align:center;font-weight:700;color:#1768e5;\">").append(coScore).append("</td>")
                        .append("<td style=\"padding:8px;text-align:center;color:#4b5563;\">").append(secAvg).append("</td>")
                        .append("<td style=\"padding:8px;text-align:center;color:#4b5563;\">").append(topQ).append("</td>")
                        .append("<td style=\"padding:8px;text-align:center;font-weight:700;color:").append(gapColor).append(";\">").append(gapStr).append("</td>")
                        .append("</tr>");
                    firstRow = false;
                }
                axisBenchHtml.append("</tbody></table>");
            }

            // ── Target maturity section ────────────────────────────────────────
            StringBuilder targetMaturityHtml = new StringBuilder();
            if (evaluation.getTargetMaturityLevel() != null) {
                String[] levels      = {"INITIAL", "BASIQUE", "INTERMEDIAIRE", "AVANCE", "OPTIMISE"};
                String[] levelLabels = {"Initial", "Basique", "Interm&#233;diaire", "Avanc&#233;", "Optimis&#233;"};
                String currentName = evaluation.getMaturityLevel() != null ? evaluation.getMaturityLevel().name() : "";
                String targetName  = evaluation.getTargetMaturityLevel().name();
                int currentIdx = -1, targetIdx = -1;
                for (int i = 0; i < levels.length; i++) {
                    if (levels[i].equals(currentName)) currentIdx = i;
                    if (levels[i].equals(targetName))  targetIdx  = i;
                }
                targetMaturityHtml
                    .append("<div style=\"background:#fff;border:2px solid #e8f0fe;border-radius:12px;padding:24px;margin-bottom:28px;\">")
                    .append("<h3 style=\"color:#0f2242;font-size:16px;margin:0 0 16px;\">&#127919; Maturit&#233; cible</h3>")
                    .append("<table style=\"width:100%;border-collapse:separate;border-spacing:4px;margin-bottom:16px;\"><tr>");
                for (int i = 0; i < levels.length; i++) {
                    String bg, color, fw = "700";
                    if (i == targetIdx)              { bg = "#166534"; color = "#ffffff"; }
                    else if (i == currentIdx)         { bg = "#dbeafe"; color = "#1768e5"; }
                    else if (currentIdx >= 0 && i < currentIdx) { bg = "#f0fdf4"; color = "#16a34a"; fw = "400"; }
                    else                              { bg = "#f9fafb"; color = "#9ca3af"; fw = "400"; }
                    targetMaturityHtml
                        .append("<td style=\"background:").append(bg).append(";color:").append(color)
                        .append(";font-weight:").append(fw)
                        .append(";font-size:11px;padding:8px 2px;text-align:center;border-radius:6px;\">")
                        .append(levelLabels[i]).append("</td>");
                }
                targetMaturityHtml
                    .append("</tr></table>")
                    .append("<table style=\"width:100%;border-collapse:collapse;\">")
                    .append("<tr><td style=\"padding:6px 0;color:#6b7280;font-size:13px;\">Niveau actuel</td>")
                    .append("<td style=\"padding:6px 0;font-weight:700;color:#1768e5;text-align:right;\">").append(currentName.isEmpty() ? "&#8212;" : currentName).append("</td></tr>")
                    .append("<tr style=\"border-top:1px solid #f1f5f9;\"><td style=\"padding:6px 0;color:#6b7280;font-size:13px;\">Maturit&#233; cible</td>")
                    .append("<td style=\"padding:6px 0;font-weight:700;color:#166534;text-align:right;\">").append(targetName).append("</td></tr>")
                    .append("</table>");
                if (currentIdx >= 0 && targetIdx > currentIdx) {
                    int gap = targetIdx - currentIdx;
                    targetMaturityHtml
                        .append("<p style=\"color:#4b5563;font-size:13px;margin:12px 0 0;line-height:1.6;\">")
                        .append("Votre consultant a d&#233;fini le niveau <strong>").append(levelLabels[targetIdx])
                        .append("</strong> comme objectif de transformation. ")
                        .append(gap == 1 ? "C&#39;est l&#39;&#233;tape suivante de votre parcours." : "Cela repr&#233;sente " + gap + " niveaux de progression.")
                        .append("</p>");
                }
                targetMaturityHtml.append("</div>");
            }

            // ── Assemble final HTML ─────────────────────────────────────────────
            String html = """
                <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:620px;margin:0 auto;background:#f8faff;border-radius:16px;overflow:hidden;">
                  <div style="background:linear-gradient(135deg,#0f2242 0%%,#1768e5 100%%);padding:36px 40px;text-align:center;">
                    <h1 style="color:#fff;margin:0;font-size:26px;font-weight:800;">IA Benchmark</h1>
                    <p style="color:rgba(255,255,255,0.75);margin:8px 0 0;font-size:14px;">Résultats d'évaluation de maturité digitale</p>
                  </div>
                  <div style="padding:40px;">
                    <h2 style="color:#0f2242;font-size:20px;margin:0 0 8px;">Bonjour, %s !</h2>
                    <p style="color:#4b5563;line-height:1.7;margin:0 0 28px;">
                      Votre consultant a analysé et validé les résultats de votre évaluation de maturité digitale.
                      Voici votre synthèse personnalisée.
                    </p>

                    <!-- Scores -->
                    <div style="background:#fff;border:2px solid #e8f0fe;border-radius:12px;padding:24px;margin-bottom:28px;">
                      <h3 style="color:#0f2242;font-size:16px;margin:0 0 16px;">&#128202; Vos scores</h3>
                      <div style="text-align:center;margin-bottom:20px;">
                        <div style="font-size:48px;font-weight:900;color:#1768e5;">%s<span style="font-size:24px;color:#6b7280;">/100</span></div>
                        <div style="color:#6b7280;font-size:13px;">Score global</div>
                        <div style="display:inline-block;background:#e8f0fe;color:#1768e5;font-weight:700;padding:4px 16px;border-radius:20px;margin-top:8px;font-size:13px;">Niveau %s</div>
                      </div>
                      <table style="width:100%%;border-collapse:collapse;">%s</table>
                    </div>

                    <!-- Benchmarking -->
                    <div style="background:#fff;border:2px solid #e8f0fe;border-radius:12px;padding:24px;margin-bottom:28px;">
                      <h3 style="color:#0f2242;font-size:16px;margin:0 0 16px;">&#127757; Positionnement sectoriel</h3>
                      <table style="width:100%%;border-collapse:collapse;">
                        <tr>
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Moyenne nationale</td>
                          <td style="padding:8px 0;font-weight:700;color:#0f2242;text-align:right;">%s/100</td>
                        </tr>
                        <tr style="border-top:1px solid #f1f5f9;">
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Moyenne internationale</td>
                          <td style="padding:8px 0;font-weight:700;color:#0f2242;text-align:right;">%s/100</td>
                        </tr>
                        <tr style="border-top:1px solid #f1f5f9;">
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Top quartile</td>
                          <td style="padding:8px 0;font-weight:700;color:#0f2242;text-align:right;">%s/100</td>
                        </tr>
                        <tr style="border-top:1px solid #f1f5f9;">
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Votre positionnement</td>
                          <td style="padding:8px 0;font-weight:700;color:#1768e5;text-align:right;">%s</td>
                        </tr>
                        <tr style="border-top:1px solid #f1f5f9;">
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Percentile</td>
                          <td style="padding:8px 0;font-weight:700;color:#1768e5;text-align:right;">%s</td>
                        </tr>
                      </table>
                      %s
                    </div>

                    <!-- Target maturity -->
                    %s

                    <!-- Recommendations -->
                    <div style="background:#f8faff;border-radius:12px;padding:24px;margin-bottom:28px;">
                      <h3 style="color:#0f2242;font-size:16px;margin:0 0 16px;">&#128161; Recommandations de votre consultant</h3>
                      %s
                    </div>

                    <!-- CTA buttons -->
                    <div style="text-align:center;margin:28px 0;">
                      <a href="http://localhost:4200/results/%s"
                         style="display:inline-block;background:linear-gradient(135deg,#0f2242 0%%,#1768e5 100%%);color:#fff;text-decoration:none;padding:14px 32px;border-radius:30px;font-size:15px;font-weight:700;margin-bottom:12px;">
                        Consulter mes résultats en ligne
                      </a>
                    </div>
                    <p style="color:#6b7280;font-size:12px;text-align:center;margin:0 0 24px;">
                      %s
                    </p>
                  </div>
                  <div style="background:#f1f5f9;padding:20px 40px;text-align:center;">
                    <p style="color:#9ca3af;font-size:12px;margin:0;">© 2025 IA Benchmark — Ne pas répondre à cet email</p>
                  </div>
                </div>
                """;

            String pdfNote = (pdfBytes != null && pdfBytes.length > 0)
                    ? "Votre rapport PDF complet est joint à cet email."
                    : "Connectez-vous sur la plateforme pour télécharger votre rapport PDF complet.";
            html = html.formatted(
                    companyName,
                    globalScore, maturity, axesHtml.toString(),
                    nationalAvg, intlAvg, topQuartile, positioning, percentile,
                    axisBenchHtml.toString(),
                    targetMaturityHtml.toString(),
                    recsHtml.toString(),
                    evaluationId,
                    pdfNote);
            helper.setText(Objects.requireNonNull(html), true);
            if (pdfBytes != null && pdfBytes.length > 0) {
                String filename = "rapport-evaluation-" + companyName.replaceAll("[^a-zA-Z0-9]", "_") + ".pdf";
                helper.addAttachment(filename, new ByteArrayResource(pdfBytes), "application/pdf");
            }
            mailSender.send(message);
        } catch (MessagingException e) {
            throw new RuntimeException("Échec de l'envoi de l'email de résultats : " + e.getMessage(), e);
        }
    }

    public void sendPasswordResetCode(String toEmail, String code) {
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setFrom(Objects.requireNonNull(fromAddress));
            helper.setTo(Objects.requireNonNull(toEmail));
            helper.setSubject("Code de réinitialisation — IA Benchmark");

            String html = """
                <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:520px;margin:0 auto;background:#f8faff;border-radius:16px;overflow:hidden;">
                  <div style="background:linear-gradient(135deg,#0f2242 0%%,#1768e5 100%%);padding:36px 40px;text-align:center;">
                    <h1 style="color:#fff;margin:0;font-size:26px;font-weight:800;letter-spacing:-0.5px;">IA Benchmark</h1>
                    <p style="color:rgba(255,255,255,0.75);margin:8px 0 0;font-size:14px;">Plateforme d'analyse IA</p>
                  </div>
                  <div style="padding:40px;">
                    <h2 style="color:#0f2242;font-size:20px;margin:0 0 12px;">Réinitialisation de mot de passe</h2>
                    <p style="color:#4b5563;line-height:1.7;margin:0 0 28px;">
                      Vous avez demandé à réinitialiser votre mot de passe. Utilisez le code ci-dessous.
                      Il est valable pendant <strong>15 minutes</strong>.
                    </p>
                    <div style="background:#fff;border:2px solid #e8f0fe;border-radius:12px;padding:24px;text-align:center;margin-bottom:28px;">
                      <p style="color:#6b7280;font-size:13px;margin:0 0 10px;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Votre code</p>
                      <span style="font-size:42px;font-weight:900;letter-spacing:10px;color:#1768e5;">%s</span>
                    </div>
                    <p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">
                      Si vous n'avez pas effectué cette demande, ignorez simplement cet email.
                      Votre mot de passe ne sera pas modifié.
                    </p>
                  </div>
                  <div style="background:#f1f5f9;padding:20px 40px;text-align:center;">
                    <p style="color:#9ca3af;font-size:12px;margin:0;">© 2025 IA Benchmark — Ne pas répondre à cet email</p>
                  </div>
                </div>
                """.formatted(code);

            helper.setText(Objects.requireNonNull(html), true);
            mailSender.send(message);

        } catch (MessagingException e) {
            throw new RuntimeException("Échec de l'envoi de l'email : " + e.getMessage(), e);
        }
    }
}
