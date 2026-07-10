#!/bin/bash

set -e

echo "=========================================="
echo " Initializing FamilyOS repository..."
echo "=========================================="

########################################
# Root directories
########################################

directories=(
".github"

"docs"
"docs/vision"
"docs/architecture"
"docs/business"
"docs/product"
"docs/roadmap"
"docs/security"
"docs/privacy"
"docs/legal"
"docs/api"
"docs/database"
"docs/deployment"
"docs/operations"
"docs/ux"
"docs/ui"
"docs/research"
"docs/meeting-notes"
"docs/adr"
"docs/diagrams"
"docs/features"
"docs/glossary"

"backend"
"backend/src"
"backend/services"
"backend/authentication"
"backend/users"
"backend/families"
"backend/calendar"
"backend/events"
"backend/tasks"
"backend/documents"
"backend/media"
"backend/notifications"
"backend/assistant"
"backend/settings"
"backend/common"
"backend/core"
"backend/config"

"frontend"
"frontend/src"
"frontend/components"
"frontend/pages"
"frontend/layouts"
"frontend/hooks"
"frontend/styles"
"frontend/assets"
"frontend/public"
"frontend/services"

"mobile"
"mobile/android"
"mobile/ios"
"mobile/flutter"
"mobile/shared"

"ai"
"ai/agents"
"ai/assistant"
"ai/prompts"
"ai/models"
"ai/memory"
"ai/rag"
"ai/evaluation"
"ai/datasets"

"api"
"api/openapi"
"api/postman"
"api/examples"
"api/reference"

"database"
"database/schema"
"database/migrations"
"database/seeds"
"database/erd"
"database/backup"

"infrastructure"
"infrastructure/docker"
"infrastructure/kubernetes"
"infrastructure/terraform"
"infrastructure/network"
"infrastructure/logging"
"infrastructure/monitoring"

"deployment"
"deployment/development"
"deployment/staging"
"deployment/production"

"shared"
"tests"
"tests/unit"
"tests/integration"
"tests/e2e"
"tests/performance"
"tests/security"

"scripts"
"assets"
"tools"
"examples"
)

########################################
# Create directories
########################################

for dir in "${directories[@]}"
do
    mkdir -p "$dir"
done

########################################
# Create README.md in each directory
########################################

find . -type d ! -path "./.git*" | while read dir
do
    if [ ! -f "$dir/README.md" ]; then
        echo "# $(basename "$dir")" > "$dir/README.md"
    fi
done

########################################
# Create root files
########################################

touch CONTRIBUTING.md
touch SECURITY.md
touch CODE_OF_CONDUCT.md
touch CHANGELOG.md
touch .gitignore

echo ""
echo "✅ FamilyOS repository initialized successfully."