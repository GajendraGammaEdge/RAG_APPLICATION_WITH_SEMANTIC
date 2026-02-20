# TODO: Fix Docker Build Timeout Issue

## Task
Fix the Poetry install timeout error during Docker build by using CPU-only PyTorch.

## Steps
- [ ] 1. Update pyproject.toml to add CPU-only torch dependency
- [ ] 2. Remove old poetry.lock file
- [ ] 3. Generate new poetry.lock without CUDA dependencies
- [ ] 4. Verify the lock file doesn't contain nvidia packages

