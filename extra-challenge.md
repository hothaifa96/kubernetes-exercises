# Hard Exercise (Milestone 7 / Instructor Challenge)

Complete milestones 1-6 first. Then pick at least two of the challenges below.

## 1. Convert MongoDB to a StatefulSet

- Replace the `mongo` Deployment with a `StatefulSet`.
- Use a `volumeClaimTemplate` so each MongoDB replica gets its own stable persistent storage.
- Use a headless Service for MongoDB discovery.
- Make the backend connect to the MongoDB replica set (optional: add a secondary replica).

## 2. Add network policies

- Restrict the frontend to only talk to the backend.
- Restrict the backend to only talk to MongoDB and Redis.
- Deny all other inter-pod traffic by default.
- Test that the UI still works.

## 3. Add liveness and readiness probes

- Add `/api/health` as a readiness probe for the backend.
- Add an HTTP liveness probe to the frontend.
- Add an `exec` liveness probe to MongoDB.
- Verify that a failing backend is taken out of service.

## 4. Implement a HorizontalPodAutoscaler

- Add CPU resource requests and limits to frontend and backend.
- Add a `HorizontalPodAutoscaler` for the backend (or frontend).
- Generate load and watch the pods scale.

## 5. Replace the Node/Express frontend with nginx

- Keep the same HTML but serve it with `nginx:alpine`.
- Use an nginx template and `envsubst` to inject `API_BASE` at startup.
- Shrink the final image size.

## 6. Secure the Ingress with TLS

- Create a self-signed certificate as a Kubernetes TLS Secret.
- Update the Ingress to use HTTPS.
- Access the application over `https://class.local`.

## Expected deliverable

A short write-up (one page) or a set of extra manifests explaining what you changed and why. Include the `kubectl` commands you used to verify the result.
