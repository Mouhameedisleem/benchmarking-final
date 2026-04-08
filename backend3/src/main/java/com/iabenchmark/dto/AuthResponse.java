package com.iabenchmark.dto;

import java.util.List;

public class AuthResponse {
    private String token;
    private String type = "Bearer";
    private Long id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private String role;
    private Long companyId;
    private String companyName;
    private List<String> roles;

    public AuthResponse(String token, Long id, String username, String email, String firstName, String lastName,
                        String role, Long companyId, String companyName, List<String> roles) {
        this.token = token;
        this.id = id;
        this.username = username;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.role = role;
        this.companyId = companyId;
        this.companyName = companyName;
        this.roles = roles;
    }

    public String getToken() { return token; }
    public String getType() { return type; }
    public Long getId() { return id; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public String getRole() { return role; }
    public Long getCompanyId() { return companyId; }
    public String getCompanyName() { return companyName; }
    public List<String> getRoles() { return roles; }
}
