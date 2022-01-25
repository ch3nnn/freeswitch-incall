# freeswitch-incall
#### Python版 freeswitch outbound 呼入服务 



##### freeswitch 配置文件
新增 freeswitch/conf/dialplan/public/1010_inbound.xml
expression 这里配置网关名称
```xml
<include>
  <extension name="1010_inbound">
    <condition field="destination_number" expression="^(配置网关)$">
        <action application="set" data="enable_heartbeat_events=true"/>
        <action application="log" data="expression: ${expression}"/>
        <action application="log" data="gateway: ${gateway}"/>
        <action application="set" data="inner_user=1008"/>
        <action application="info" data=""/>
        <action application="socket" data="127.0.0.1:8050 async full"/>
    </condition>
  </extension>
</include>
```

##### 运行命令
```shell
sh runserver.sh
```