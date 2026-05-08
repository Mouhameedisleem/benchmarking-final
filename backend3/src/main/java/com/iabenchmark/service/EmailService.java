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
import java.util.List;

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
            helper.setFrom(fromAddress);
            helper.setTo(toEmail);
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

            helper.setText(html, true);
            mailSender.send(message);
        } catch (MessagingException e) {
            throw new RuntimeException("Échec de l'envoi de l'email : " + e.getMessage(), e);
        }
    }

    public void sendEvaluationResults(String toEmail, String companyName,
                                      Evaluation evaluation,
                                      List<RecommendationResponse> recommendations,
                                      BenchmarkResponse benchmark) {
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            helper.setFrom(fromAddress);
            helper.setTo(toEmail);
            helper.setSubject("Vos résultats d'évaluation de maturité digitale — " + companyName);

            String maturity = evaluation.getMaturityLevel() != null ? evaluation.getMaturityLevel().name() : "—";
            String globalScore = String.format("%.1f", evaluation.getGlobalScore());
            String businessScore = String.format("%.1f", evaluation.getBusinessScore());
            String processScore = String.format("%.1f", evaluation.getProcessScore());
            String siScore = String.format("%.1f", evaluation.getInformationSystemScore());

            StringBuilder recsHtml = new StringBuilder();
            if (recommendations != null && !recommendations.isEmpty()) {
                for (RecommendationResponse rec : recommendations) {
                    String badgeColor = "HAUTE".equals(rec.getPriority()) ? "#dc2626"
                            : "MOYENNE".equals(rec.getPriority()) ? "#d97706" : "#16a34a";
                    recsHtml.append("""
                        <div style="border-left:4px solid %s;padding:12px 16px;margin-bottom:12px;background:#fff;border-radius:0 8px 8px 0;">
                          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                            <span style="background:%s;color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;">%s</span>
                            <span style="font-weight:700;color:#0f2242;font-size:14px;">%s</span>
                          </div>
                          <p style="color:#4b5563;font-size:13px;margin:0 0 6px;">%s</p>
                          <p style="color:#6b7280;font-size:12px;margin:0;font-style:italic;">%s</p>
                        </div>
                        """.formatted(badgeColor, badgeColor, rec.getPriority(),
                            rec.getTitle(), rec.getDescription(), rec.getBestPractice()));
                }
            } else {
                recsHtml.append("<p style='color:#6b7280;font-size:13px;'>Aucune recommandation disponible.</p>");
            }

            String nationalAvg = benchmark != null && benchmark.getSectorBenchmark() != null
                    ? String.format("%.1f", benchmark.getSectorBenchmark().getNationalAverage()) : "—";
            String intlAvg = benchmark != null && benchmark.getSectorBenchmark() != null
                    ? String.format("%.1f", benchmark.getSectorBenchmark().getInternationalAverage()) : "—";
            String positioning = benchmark != null && benchmark.getSectorBenchmark() != null
                    ? benchmark.getSectorBenchmark().getPositioningLabel() : "—";

            String html = """
                <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#f8faff;border-radius:16px;overflow:hidden;">
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
                      <h3 style="color:#0f2242;font-size:16px;margin:0 0 16px;">📊 Vos scores</h3>
                      <div style="text-align:center;margin-bottom:16px;">
                        <div style="font-size:48px;font-weight:900;color:#1768e5;">%s<span style="font-size:24px;color:#6b7280;">/100</span></div>
                        <div style="color:#6b7280;font-size:13px;">Score global</div>
                        <div style="display:inline-block;background:#e8f0fe;color:#1768e5;font-weight:700;padding:4px 16px;border-radius:20px;margin-top:8px;font-size:13px;">Niveau %s</div>
                      </div>
                      <table style="width:100%%;border-collapse:collapse;">
                        <tr>
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Axe Métier</td>
                          <td style="padding:8px 0;font-weight:700;color:#0f2242;text-align:right;">%s/100</td>
                        </tr>
                        <tr style="border-top:1px solid #f1f5f9;">
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Axe Processus</td>
                          <td style="padding:8px 0;font-weight:700;color:#0f2242;text-align:right;">%s/100</td>
                        </tr>
                        <tr style="border-top:1px solid #f1f5f9;">
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Axe Système d'Information</td>
                          <td style="padding:8px 0;font-weight:700;color:#0f2242;text-align:right;">%s/100</td>
                        </tr>
                      </table>
                    </div>

                    <!-- Benchmarking -->
                    <div style="background:#fff;border:2px solid #e8f0fe;border-radius:12px;padding:24px;margin-bottom:28px;">
                      <h3 style="color:#0f2242;font-size:16px;margin:0 0 16px;">🌍 Positionnement sectoriel</h3>
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
                          <td style="padding:8px 0;color:#6b7280;font-size:13px;">Votre positionnement</td>
                          <td style="padding:8px 0;font-weight:700;color:#1768e5;text-align:right;">%s</td>
                        </tr>
                      </table>
                    </div>

                    <!-- Recommendations -->
                    <div style="background:#f8faff;border-radius:12px;padding:24px;margin-bottom:28px;">
                      <h3 style="color:#0f2242;font-size:16px;margin:0 0 16px;">💡 Recommandations de votre consultant</h3>
                      %s
                    </div>

                    <p style="color:#4b5563;font-size:13px;line-height:1.7;margin:0 0 24px;">
                      Connectez-vous sur <a href="http://localhost:4200/login" style="color:#1768e5;">la plateforme</a>
                      pour consulter votre rapport complet et télécharger votre bilan PDF.
                    </p>
                  </div>
                  <div style="background:#f1f5f9;padding:20px 40px;text-align:center;">
                    <p style="color:#9ca3af;font-size:12px;margin:0;">© 2025 IA Benchmark — Ne pas répondre à cet email</p>
                  </div>
                </div>
                """.formatted(companyName, globalScore, maturity,
                    businessScore, processScore, siScore,
                    nationalAvg, intlAvg, positioning,
                    recsHtml.toString());

            helper.setText(html, true);
            mailSender.send(message);
        } catch (MessagingException e) {
            throw new RuntimeException("Échec de l'envoi de l'email de résultats : " + e.getMessage(), e);
        }
    }

    public void sendPasswordResetCode(String toEmail, String code) {
        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setFrom(fromAddress);
            helper.setTo(toEmail);
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

            helper.setText(html, true);
            mailSender.send(message);

        } catch (MessagingException e) {
            throw new RuntimeException("Échec de l'envoi de l'email : " + e.getMessage(), e);
        }
    }
}
