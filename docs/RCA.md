# Root Cause Analysis

## Summary
Redirects failed due to URL being marked inactive, causing error spikes.

## Timeline
23:01 - Alert triggered  
23:03 - Redirect errors observed  
23:04 - Grafana confirms spike  
23:05 - Event log shows is_active=false  
23:06 - URL reactivated  
23:07 - Errors resolved  

## Root Cause
URL was set to inactive via update event.

## Fix
Reactivated URL and monitored.

## Prevention
Improved logging, dashboard indicators, and updated runbook.
