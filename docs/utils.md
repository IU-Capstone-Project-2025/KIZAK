# Utils API

## `GET /skills_list/`

**Summary**: Retrieve a list of all available skills from the ML service.

**Method**: GET

**Tags**: Utility

**Description**: Makes a request to the internal ML service to get user skills.

**Example Request**:

```bash
curl -X GET "https://api.example.com/skills_list/"
```

### Responses:

* **200 OK**

    * **Content**: JSON list of skills (from ML service)

  ```json
  ["Python", "Machine Learning", "Docker", "FastAPI"]
  ```

---

## `GET /check_login/{login}`

**Summary**: Check if a user with the specified login exists.

**Method**: GET

**Tags**: Utility

**Path Parameter**:

* `login` (string) – Login to check.

**Example Request**:

```bash
curl -X GET "https://api.example.com/check_login/johndoe"
```

### Responses:

* **200 OK**

  ```json
  {
    "exists": true
  }
  ```

  or

  ```json
  {
    "exists": false
  }
  ```

---

## `GET /check_email/{email}`

**Summary**: Check if a user with the specified email exists.

**Method**: GET

**Tags**: Utility

**Path Parameter**:

* `email` (string) – Email to check.

**Example Request**:

```bash
curl -X GET "https://api.example.com/check_email/user@example.com"
```

### Responses:

* **200 OK**

  ```json
  {
    "exists": true
  }
  ```

  or

  ```json
  {
    "exists": false
  }
  ```
