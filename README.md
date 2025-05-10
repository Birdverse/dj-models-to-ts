# dj-models-to-ts
Auto-generate TypeScript interfaces from Django models for use in modern frontend apps like SvelteKit or Next.js.

## Why Use This

- Keep backend and frontend types in sync
- Improve frontend autocompletion and contract enforcement
- Simplify working with Django REST Framework or similar APIs in TypeScript projects

## Works With

- Django (including multi-app projects)
- SvelteKit / React / Next.js / Vue (any TypeScript-based frontend)

## Setup

1. Copy `generate_ts_models.py` into your backend project.
2. Adjust the config at the top of the script:

```python
BACKEND_DIR = "api/models"  # or "apps" or "myproject/apps"
FRONTEND_DIR = "../frontend/src/lib/types/models"
```

3. Run it:

```bash
python generate_ts_models.py
```

4. Interfaces will appear in your frontend project. Commit and import as needed.

## Notes

- Maps basic Django fields (extend `FIELD_TYPE_MAP` for custom types)
- ForeignKey/OneToOne become `number`
- ManyToMany becomes `number[]`
- Defaults to `any` if field type is unknown

## Example

Given:

```python
class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
```

You'll get:

```ts
export interface Course {
  name?: string;
  teacher?: number;
}
```

---

PRs and improvements welcome.
