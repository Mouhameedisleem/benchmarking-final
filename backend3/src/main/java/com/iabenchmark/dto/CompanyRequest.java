package com.iabenchmark.dto;

import jakarta.validation.constraints.NotBlank;

public class CompanyRequest {
    @NotBlank(message = "Company name is required")
    private String name;

    @NotBlank(message = "Sector is required")
    private String sector;

    @NotBlank(message = "Country is required")
    private String country;

    @NotBlank(message = "Size is required")
    private String size;

    @NotBlank(message = "Business domain is required")
    private String businessDomain;

    private String website;
    private String phone;
    private String email;
    private String address;
    private Long consultantId;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }
    public String getBusinessDomain() { return businessDomain; }
    public void setBusinessDomain(String businessDomain) { this.businessDomain = businessDomain; }
    public String getWebsite() { return website; }
    public void setWebsite(String website) { this.website = website; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }
    public Long getConsultantId() { return consultantId; }
    public void setConsultantId(Long consultantId) { this.consultantId = consultantId; }
}
