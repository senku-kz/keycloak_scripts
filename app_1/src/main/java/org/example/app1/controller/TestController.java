package org.example.app1.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.security.access.prepost.PreAuthorize;

@RestController
public class TestController {
    @GetMapping("/message")
    @PreAuthorize("hasAuthority('SCOPE_openid')")
    public String getMessage() {
        return "Hello from App 1!";
    }
}
