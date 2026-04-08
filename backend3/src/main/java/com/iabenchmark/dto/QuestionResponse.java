package com.iabenchmark.dto;

import com.iabenchmark.model.QuestionAxis;

public class QuestionResponse {
    private Long id;
    private String text;
    private QuestionAxis axis;
    private String subAxis;
    private Integer weight;
    private Integer displayOrder;

    public QuestionResponse(Long id, String text, QuestionAxis axis, String subAxis, Integer weight, Integer displayOrder) {
        this.id = id;
        this.text = text;
        this.axis = axis;
        this.subAxis = subAxis;
        this.weight = weight;
        this.displayOrder = displayOrder;
    }

    public Long getId() { return id; }
    public String getText() { return text; }
    public QuestionAxis getAxis() { return axis; }
    public String getSubAxis() { return subAxis; }
    public Integer getWeight() { return weight; }
    public Integer getDisplayOrder() { return displayOrder; }
}
