package com.iabenchmark.dto;

import com.iabenchmark.model.QuestionAxis;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.List;

public class QuestionRequest {
    @NotBlank(message = "Question text is required")
    private String text;

    @NotNull(message = "Question axis is required")
    private QuestionAxis axis;

    @NotBlank(message = "Question sub-axis is required")
    private String subAxis;

    @NotNull(message = "Question weight is required")
    @Min(value = 1, message = "Question weight must be at least 1")
    @Max(value = 100, message = "Question weight must not exceed 100")
    private Integer weight;

    @NotNull(message = "Question display order is required")
    @Min(value = 1, message = "Question display order must be at least 1")
    private Integer displayOrder;

    private List<String> options;

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
    public QuestionAxis getAxis() { return axis; }
    public void setAxis(QuestionAxis axis) { this.axis = axis; }
    public String getSubAxis() { return subAxis; }
    public void setSubAxis(String subAxis) { this.subAxis = subAxis; }
    public Integer getWeight() { return weight; }
    public void setWeight(Integer weight) { this.weight = weight; }
    public Integer getDisplayOrder() { return displayOrder; }
    public void setDisplayOrder(Integer displayOrder) { this.displayOrder = displayOrder; }
    public List<String> getOptions() { return options; }
    public void setOptions(List<String> options) { this.options = options; }
}
