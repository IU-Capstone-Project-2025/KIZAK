# Mail API

## `POST /send_mail/`

**Summary**: Sends a welcome email to one or more recipients.

**Method**: POST

**Tags**: Mail

**Request Body**:

* `EmailModel`

    * `addresses` (List\[str]) – A list of recipient email addresses.

**Example Request Body**:

```json
{
  "addresses": ["user1@example.com", "user2@example.com"]
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/send_mail/" \
  -H "Content-Type: application/json" \
  -d '{
        "addresses": ["user1@example.com", "user2@example.com"]
      }'
```

### Responses:

* **200 OK**

    * **Content**:

      ```json
      {
        "message": "Email sent successfully"
      }
      ```

* **422 Unprocessable Entity**

    * **Example Response**:

      ```json
      {
        "detail": [
          {
            "loc": ["body", "addresses"],
            "msg": "field required",
            "type": "value_error.missing"
          }
        ]
      }
      ```
