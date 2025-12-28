targetScope = 'subscription'

@description('Azure region for all resources')
param location string = 'westeurope'

@description('Resource group name')
param rgName string

@description('Common tags')
param tags object = {}

@description('Globally-unique storage account name (lowercase, 3-24 chars)')
param storageAccountName string

@description('Globally-unique Key Vault name (3-24 chars, alphanum + hyphen, must start with letter)')
param keyVaultName string

@description('Globally-unique SQL server name')
param sqlServerName string

@description('SQL database name')
param sqlDbName string = 'tradingdb'

@description('SQL admin username (SQL auth). Keep for bootstrap; later switch apps to Entra ID auth.')
param sqlAdminLogin string

@secure()
@description('SQL admin password (SQL auth). Pass via CLI or pipeline secret.')
param sqlAdminPassword string

// Resource group (subscription scope)
resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: rgName
  location: location
  tags: tags
}

// Deploy all RG-scoped resources via module
module core 'core-rg.bicep' = {
  name: 'core-rg'
  scope: rg
  params: {
    location: location
    tags: tags
    storageAccountName: storageAccountName
    keyVaultName: keyVaultName
    sqlServerName: sqlServerName
    sqlDbName: sqlDbName
    sqlAdminLogin: sqlAdminLogin
    sqlAdminPassword: sqlAdminPassword
    logAnalyticsName: 'law-${rgName}'
  }
}

output resourceGroupName string = rg.name
output sqlServerFqdn string = core.outputs.sqlServerFqdn
output storageAccountNameOut string = core.outputs.storageAccountName
output keyVaultNameOut string = core.outputs.keyVaultName
