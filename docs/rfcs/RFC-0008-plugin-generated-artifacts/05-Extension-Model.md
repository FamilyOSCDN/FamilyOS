# Extension Model

## Plugin Recipe Extension

A plugin may provide:

GenerationRecipe

Example responsibility:

A healthcare plugin may provide:

- HealthcareReportRecipe
- MedicalSummaryRecipe


## Registry Flow

Plugin

↓

PluginContributionProvider

↓

ContributionRegistry

↓

GenerationRecipeContribution

↓

GenerationRecipeRegistry


## Built-in Recipes

Built-in recipes remain managed by FamilyOS.

Plugin recipes extend the registry but do not replace it.
