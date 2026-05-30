package com.iabenchmark.service;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class NotificationSseService {

    private final ConcurrentHashMap<Long, CopyOnWriteArrayList<SseEmitter>> emitters = new ConcurrentHashMap<>();

    public SseEmitter subscribe(Long userId) {
        SseEmitter emitter = new SseEmitter(Long.MAX_VALUE);
        emitters.computeIfAbsent(userId, k -> new CopyOnWriteArrayList<>()).add(emitter);

        emitter.onCompletion(() -> remove(userId, emitter));
        emitter.onTimeout(()    -> remove(userId, emitter));
        emitter.onError(e       -> remove(userId, emitter));

        // Initial connected event so the client knows the stream is live
        try {
            emitter.send(SseEmitter.event()
                    .data(Objects.requireNonNull(Map.of("type", "connected", "message", "Connecté aux notifications"))));
        } catch (IOException e) {
            remove(userId, emitter);
        }
        return emitter;
    }

    public void notifyUser(Long userId, String message, String type) {
        List<SseEmitter> targets = emitters.get(userId);
        if (targets == null || targets.isEmpty()) return;
        dispatch(targets, buildPayload(message, type));
    }

    public void notifyAllConsultantsAndAdmins(String message, String type) {
        emitters.forEach((uid, targets) -> dispatch(targets, buildPayload(message, type)));
    }

    // ── Keep-alive heartbeat every 20 s ──────────────────────────────────────
    @Scheduled(fixedDelay = 20_000)
    public void heartbeat() {
        emitters.forEach((uid, targets) -> {
            List<SseEmitter> dead = new ArrayList<>();
            for (SseEmitter e : targets) {
                try { e.send(SseEmitter.event().comment("heartbeat")); }
                catch (Exception ex) { dead.add(e); }
            }
            targets.removeAll(dead);
        });
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private void dispatch(List<SseEmitter> targets, Map<String, Object> payload) {
        List<SseEmitter> dead = new ArrayList<>();
        for (SseEmitter e : targets) {
            try { e.send(SseEmitter.event().data(Objects.requireNonNull(payload))); }
            catch (Exception ex) { dead.add(e); }
        }
        targets.removeAll(dead);
    }

    private Map<String, Object> buildPayload(String message, String type) {
        return Map.of(
                "id",        UUID.randomUUID().toString(),
                "message",   message,
                "type",      type,
                "timestamp", LocalDateTime.now().toString()
        );
    }

    private void remove(Long userId, SseEmitter emitter) {
        CopyOnWriteArrayList<SseEmitter> list = emitters.get(userId);
        if (list != null) list.remove(emitter);
    }
}
