# 🔐 Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

We take the security of Auto-SignIn seriously. If you have discovered a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them using one of the following methods:

1. **GitHub Security Advisory** (Preferred)
   - Go to the [Security Advisories](https://github.com/badhope/Auto-SignIn/security/advisories) page
   - Click "Report a vulnerability"
   - Fill in the details of the vulnerability

2. **Email**
   - Send an email to the project maintainer
   - Include "SECURITY" in the subject line
   - Provide detailed information about the vulnerability

### What to Include

When reporting a vulnerability, please include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** of the vulnerability
- **Possible solutions** (if you have any)
- **Your contact information** (for follow-up questions)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Timeline**: Depends on severity
  - Critical: 7-14 days
  - High: 14-30 days
  - Medium: 30-60 days
  - Low: Next release

### What to Expect

1. **Acknowledgment**: We will acknowledge receipt of your report
2. **Investigation**: We will investigate the issue
3. **Updates**: We will keep you informed of our progress
4. **Resolution**: We will fix the issue and release a patch
5. **Disclosure**: We will publicly disclose the issue after the fix is released

### Disclosure Policy

- We follow **Responsible Disclosure**
- We ask that you do not publicly disclose the vulnerability until we have had a chance to fix it
- We will credit you in the security advisory (unless you prefer to remain anonymous)

### Security Best Practices

When using Auto-SignIn, please follow these security best practices:

#### Cookie Security

- **Never share your cookies** with others
- **Regularly rotate** your cookies
- **Use environment variables** to store sensitive information
- **Enable cookie expiration** notifications

#### Configuration Security

- **Don't commit** `config.yml` to version control
- **Use environment variables** for sensitive data
- **Restrict file permissions** on configuration files
- **Use Docker secrets** when deploying with Docker

#### Deployment Security

- **Keep dependencies updated**
- **Use HTTPS** for all connections
- **Run as non-root user** in Docker
- **Enable firewall rules** to restrict access

#### Account Security

- **Use strong passwords** for your accounts
- **Enable two-factor authentication** where available
- **Monitor account activity** regularly
- **Report suspicious activity** immediately

### Known Security Considerations

#### Cookie Storage

- Cookies are stored in local configuration files
- Ensure proper file permissions (600 or 400)
- Consider using encrypted storage solutions

#### Network Security

- All API requests use HTTPS
- No sensitive data is logged
- Network errors are handled securely

#### Data Privacy

- No personal data is collected or transmitted
- All data is stored locally
- You have full control over your data

### Security Updates

Security updates will be released:

- As **patch releases** for supported versions
- Announced in **GitHub Releases**
- Documented in **CHANGELOG.md**
- Tagged with **security** label

### Contact

For any security-related questions or concerns:

- **GitHub Security**: [Security Advisories](https://github.com/badhope/Auto-SignIn/security/advisories)
- **Issues**: For non-sensitive security questions, you can open an issue

---

## Security Checklist

Before deploying Auto-SignIn, ensure:

- [ ] Configuration files are not publicly accessible
- [ ] Sensitive data is stored in environment variables
- [ ] File permissions are properly set
- [ ] Dependencies are up to date
- [ ] Running as non-root user (Docker)
- [ ] Network access is properly restricted
- [ ] Logs do not contain sensitive information
- [ ] Regular security updates are applied

---

<p align="center">
  Thank you for helping keep Auto-SignIn secure! 🔐
</p>
