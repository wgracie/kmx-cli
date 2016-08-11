# 1. show meta data
```
show {device|devicetype} id
show {devices|devicetypes} [ like wildcard ]
show {devices|devicetypes} [ where key=value]
```
#
# 2. create meta data
## 2.1 create deviceType
```
create devicetype <deviceTypeId>(<sensorId> <valueType>[,<sensorId> <valueType>,...]) tags(<t1>[,...]) attributes(<k1 v1>[,...])
```
## 2.2 create device
```
create device <deviceId>(<deviceTypeId>) tags(t1[,...]) attributes(k1 v1[,...])
```
#
# 3. update meta date
## 3.1 update deviceType
```
update devicetype set tags(t1[,...]) attributes(k1 v1[,...]) where id = <deviceTypeId>
```
3.2 update device
```
update device set deviceTypeId=<deviceTypeId>,tags(t1[,...]) attributes(k1 v1[,...]) where id = <deviceId>
```
#
# 4. drop meta data
```
drop {device | devicetype} {<deviceTypeId> | <deviceId>}
```
#
# 5. import dynamic data
```
import '<csv_file_path>' into <deviceTypeId>
```
#
# 6. query dynamic data
## 6.1 data point query
```
select <sensorId>[,<sensorId>...] from <deviceId> [where ts={<timestamp> |'<iso>' | 'relative_time_expr'}]
select * from <deviceId> [where ts={<timestamp> |'<iso>' | 'relative_time_expr'}]
```
***relative_time_expr:***  ```^(now)(-)([0-9]+)([s,m,h,d,w]{1})$```


## 6.1 data range query
```
select <sensorId>[,<sensorId>...] from <deviceId> [where ts > {<timestamp> |'<iso>' | 'relative_time_expr'} and ts < {<timestamp> |'<iso>' | 'relative_time_expr'}]
select * from device_name [where ts>{<timestamp> |'<iso>' } and {<timestamp> |'<iso>' }]
```
***relative_time_expr:***  ```^(now)(-)([0-9]+)([s,m,h,d,w]{1})$```