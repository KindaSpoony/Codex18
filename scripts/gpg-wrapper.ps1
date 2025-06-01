param([Parameter(ValueFromRemainingArguments=$true)][String[]]$Args)
& gpg --batch --pinentry-mode loopback --passphrase "$env:GPG_PASSPHRASE" @Args
exit $LASTEXITCODE
