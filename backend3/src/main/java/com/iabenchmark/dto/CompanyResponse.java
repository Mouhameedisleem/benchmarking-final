package com.iabenchmark.dto;

import java.time.LocalDateTime;

public class CompanyResponse {
    private Long id;
    private String name;
    private String sector;
    private String country;
    private String size;
    private String businessDomain;
    private String website;
    private String phone;
    private String email;
    private String address;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private Long consultantId;
    private String consultantName;

    public CompanyResponse(Long id, String name, String sector, String country, String size,
                           String businessDomain, String website, String phone, String email,
                           String address, LocalDateTime createdAt, LocalDateTime updatedAt,
                           Long consultantId, String consultantName) {
        this.id = id;
        this.name = name;
        this.sector = sector;
        this.country = country;
        this.size = size;
        this.businessDomain = businessDomain;
        this.website = website;
        this.phone = phone;
        this.email = email;
        this.address = address;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.consultantId = consultantId;
        this.consultantName = consultantName;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public String getSector() { return sector; }
    public String getCountry() { return country; }
    public String getSize() { return size; }
    public String getBusinessDomain() { return businessDomain; }
    public String getWebsite() { return website; }
    public String getPhone() { return phone; }
    public String getEmail() { return email; }
    public String getAddress() { return address; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public Long getConsultantId() { return consultantId; }
    public String getConsultantName() { return consultantName; }
}
