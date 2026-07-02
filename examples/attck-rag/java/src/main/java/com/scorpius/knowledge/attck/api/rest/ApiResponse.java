package com.scorpius.knowledge.attck.api.rest;

/**
 * 统一 API 响应格式 — Scorpius 标准
 * <p>
 * 所有 REST 接口统一返回此结构: success / message / data / errorCode / timestamp
 */
public class ApiResponse<T> {

    private boolean success;
    private String message;
    private T data;
    private String errorCode;
    private long timestamp;

    private ApiResponse() {}

    public static <T> ApiResponse<T> ok(T data) {
        ApiResponse<T> resp = new ApiResponse<>();
        resp.success = true;
        resp.message = "OK";
        resp.data = data;
        resp.timestamp = System.currentTimeMillis();
        return resp;
    }

    public static <T> ApiResponse<T> fail(String errorCode, String message) {
        ApiResponse<T> resp = new ApiResponse<>();
        resp.success = false;
        resp.message = message;
        resp.errorCode = errorCode;
        resp.timestamp = System.currentTimeMillis();
        return resp;
    }

    // ---- Getters ----

    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
    public T getData() { return data; }
    public String getErrorCode() { return errorCode; }
    public long getTimestamp() { return timestamp; }
}
