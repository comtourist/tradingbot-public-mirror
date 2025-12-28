using './main.bicep'

param location = 'westeurope'
param rgName = 'rg-tradingbot-dev'

param tags = {
  project: 'TradingBot'
  env: 'dev'
}

param storageAccountName = 'sttradingbotdev001'
param keyVaultName = 'kv-tradingbot-dev-001'
param sqlServerName = 'sql-tradingbot-dev-001'

param sqlDbName = 'tradingdb'
param sqlAdminLogin = 'sqladminuser'

// placeholder; overridden by CLI
param sqlAdminPassword = ''
