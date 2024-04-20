---
draft: true
date: 2024-03-06
slug: looker-download-tracking
tags:
  - "#looker"
authors:
  - Prabha
---
# Question: Is there a way to track the user downloads in Looker?

Response from Looker Support Below:
So, there is no direct way to track download activities. This is currently a Feature Request - [https://portal.feedback.us.pendo.io/app/#/case/190687](https://portal.feedback.us.pendo.io/app/#/case/190687)

However, we have a workaround using System Activity Event Attribute explore, please check the link - [https://madhive.cloud.looker.com/explore/system__activity/event_attribute?fields=event.created_time,user.name,event_attribute.event_id,event_attribute.name,event_attribute.value&f[event.category]=query&f[event.created_date]=30+days&f[event.name]=export%5E_query&sorts=event.created_time&limit=5000&query_timezone=America%2FNew_York&vis=%7B%7D&filter_config=%7B%22event.category%22%3A%5B%7B%22type%22%3A%22%3D%22%2C%22values%22%3A%5B%7B%22constant%22%3A%22query%22%7D%2C%7B%7D%5D%2C%22id%22%3A0%2C%22error%22%3Afalse%7D%5D%2C%22event.created_date%22%3A%5B%7B%22type%22%3A%22past%22%2C%22values%22%3A%5B%7B%22constant%22%3A%2230%22%2C%22unit%22%3A%22day%22%7D%2C%7B%7D%5D%2C%22id%22%3A2%2C%22error%22%3Afalse%7D%5D%2C%22event.name%22%3A%5B%7B%22type%22%3A%22%3D%22%2C%22values%22%3A%5B%7B%22constant%22%3A%22export_query%22%7D%2C%7B%7D%5D%2C%22id%22%3A4%2C%22error%22%3Afalse%7D%5D%7D&dynamic_fields=%5B%5D&origin=share-expanded](https://madhive.cloud.looker.com/explore/system__activity/event_attribute?fields=event.created_time,user.name,event_attribute.event_id,event_attribute.name,event_attribute.value&f[event.category]=query&f[event.created_date]=30+days&f[event.name]=export%5E_query&sorts=event.created_time&limit=5000&query_timezone=America%2FNew_York&vis=%7B%7D&filter_config=%7B%22event.category%22%3A%5B%7B%22type%22%3A%22%3D%22%2C%22values%22%3A%5B%7B%22constant%22%3A%22query%22%7D%2C%7B%7D%5D%2C%22id%22%3A0%2C%22error%22%3Afalse%7D%5D%2C%22event.created_date%22%3A%5B%7B%22type%22%3A%22past%22%2C%22values%22%3A%5B%7B%22constant%22%3A%2230%22%2C%22unit%22%3A%22day%22%7D%2C%7B%7D%5D%2C%22id%22%3A2%2C%22error%22%3Afalse%7D%5D%2C%22event.name%22%3A%5B%7B%22type%22%3A%22%3D%22%2C%22values%22%3A%5B%7B%22constant%22%3A%22export_query%22%7D%2C%7B%7D%5D%2C%22id%22%3A4%2C%22error%22%3Afalse%7D%5D%7D&dynamic_fields=%5B%5D&origin=share-expanded)

You can also refer to- [https://www.googlecloudcommunity.com/gc/Technical-Tips-Tricks/Track-Downloads-in-System-Activity-workaround/ta-p/586869](https://www.googlecloudcommunity.com/gc/Technical-Tips-Tricks/Track-Downloads-in-System-Activity-workaround/ta-p/586869)