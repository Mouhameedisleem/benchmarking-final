package com.iabenchmark.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;

@Service
public class EmailService {

    private final JavaMailSender mailSender;

    @Value("${app.mail.from}")
    private String fromAddress;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
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
