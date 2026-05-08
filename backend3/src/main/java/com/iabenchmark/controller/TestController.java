package com.iabenchmark.controller;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/test")
public class TestController {
    @GetMapping("/all")
    public String allAccess() { return "Public Content."; }

    @GetMapping("/admin")
    @PreAuthorize("hasRole('ADMIN')")
    public String adminAccess() { return "Admin Board."; }

    @GetMapping("/consultant")
    @PreAuthorize("hasRole('CONSULTANT')")
    public String consultantAccess() { return "Consultant Board."; }
}