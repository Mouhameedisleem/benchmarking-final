package com.iabenchmark.controller;

import com.iabenchmark.security.UserDetailsImpl;
import com.iabenchmark.service.NotificationSseService;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@RestController
@RequestMapping("/api/notifications")
public class NotificationController {

    private final NotificationSseService sseService;

    public NotificationController(NotificationSseService sseService) {
        this.sseService = sseService;
    }

    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    @PreAuthorize("hasAnyRole('ADMIN', 'CONSULTANT')")
    public SseEmitter stream(@AuthenticationPrincipal UserDetailsImpl principal) {
        return sseService.subscribe(principal.getId());
    }
}
