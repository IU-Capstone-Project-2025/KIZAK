# Feedback API

## `POST /feedback/`

**Summary**: Submit user feedback.

**Method**: POST

**Tags**: Feedback

**Description**: Post users feedback

**Request Body**:

* `FeedbackCreate`

    * Example fields:

        * `user_id` (UUID) – ID of the user providing the feedback.
        * `message` (string) – Feedback text content.
        * `rating` (int) – Optional numeric rating (e.g., 1–5).

**Example Request Body**:

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": "Great platform, really helped me!",
  "rating": 5
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/feedback/" \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "message": "Great platform, really helped me!",
        "rating": 5
      }'
```

### Responses:

* **201 Created**

    * **Content**:

      ```json
      {
        "feedback_id": "abc12345-d678-9012-efgh-3456789ijkl0",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "message": "Great platform, really helped me!",
        "rating": 5,
        "created_at": "2025-07-20T12:34:56.789Z"
      }
      ```

* **422 Unprocessable Entity**

    * **Example Response**:

      ```json
      {
        "detail": [
          {
            "loc": ["body", "message"],
            "msg": "field required",
            "type": "value_error.missing"
          }
        ]
      }
      ```
