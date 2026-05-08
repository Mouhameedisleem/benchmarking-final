package com.iabenchmark.dto;

import com.iabenchmark.model.QuestionAxis;
import java.util.List;

public class QuestionResponse {
    private Long id;
    private String text;
    private QuestionAxis axis;
    private String subAxis;
    private Integer weight;
    private Integer displayOrder;
    private List<String> options;

    public QuestionResponse(Long id, String text, QuestionAxis axis, String subAxis,
                            Integer weight, Integer displayOrder, List<String> options) {
        this.id = id;
        this.text = text;
        this.axis = axis;
        this.subAxis = subAxis;
        this.weight = weight;
        this.displayOrder = displayOrder;
        this.options = options;
    }

    public Long getId() { return id; }
    public String getText() { return text; }
    public QuestionAxis getAxis() { return axis; }
    public String getSubAxis() { return subAxis; }
    public Integer getWeight() { return weight; }
    public Integer getDisplayOrder() { return displayOrder; }
    public List<String> getOptions() { return options; }
}
