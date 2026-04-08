package com.iabenchmark.dto;

import jakarta.validation.constraints.NotBlank;

public class CompanyRegistrationRequest {
    @NotBlank(message = "Company name is required")
    private String companyName;
    @NotBlank(message = "Sector is required")
    private String sector;
    @NotBlank(message = "Country is required")
    private String country;
    @NotBlank(message = "Size is required")
    private String size;
    @NotBlank(message = "Business domain is required")
    private String activityDomain;
    @NotBlank(message = "Email is required")
    private String email;
    @NotBlank(message = "Password is required")
    private String password;
    @NotBlank(message = "First name is required")
    private String firstName;
    @NotBlank(message = "Last name is required")
    private String lastName;
    private String phone;
    private String website;
    private String address;

    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }
    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }
    public String getCountry() { return country; }
    public void setCountry(String country) { this.country = country; }
    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }
    public String getActivityDomain() { return activityDomain; }
    public void setActivityDomain(String activityDomain) { this.activityDomain = activityDomain; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getWebsite() { return website; }
    public void setWebsite(String website) { this.website = website; }
    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }
}
