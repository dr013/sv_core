# Description

This is Django core template project with  Events, Notification, Processes and Reports functionality

## Setup

```bash
pip install sv_core
```

add to settings:
```javascript
INSTALLED_APPS = [
...
    'sv_core.core.com.apps.CommonConfig',
    'sv_core.core.evt.apps.EventConfig',
    'sv_core.core.ntf.apps.NotificationConfig',
    'sv_core.core.ost.apps.OrganizationalStructureConfig',
    'sv_core.core.prc.apps.ProcessConfig',
    'sv_core.core.rpt.apps.ReportConfig',
    'sv_core.core.rul.apps.RuleConfig',
    'sv_core.core.sec.apps.SecureConfig',
]
```
Prepare and run migration:
```bash
./manage.py makemigrations
./manage.py migrate
```

# Authors
Eugene Kryukov<ekryukov@icloud.com>

