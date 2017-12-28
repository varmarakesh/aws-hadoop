class HadoopConfig(object):

    @property
    def core_site_text(self):
        return """<?xml version=\\""1.0\\"" encoding=\\""UTF-8\\""?>
                        <?xml-stylesheet type=\\""text/xsl\\"" href=\\""configuration.xsl\\""?>
                        <configuration>
                        <property>
                        <name>fs.default.name</name>
                        <value>hdfs://{0}:8020</value>
                        </property>
                        <property>
                        <name>hadoop.tmp.dir</name>
                        <value>/home/ubuntu/hdfstmp</value>
                        </property>
                        </configuration>"""

    @property
    def hdfs_site_text(self):
        return """<?xml version=\\""1.0\\"" encoding=\\""UTF-8\\""?>
                        <?xml-stylesheet type=\\""text/xsl\\"" href=\\""configuration.xsl\\""?>
                        <configuration>
                        <property>
                        <name>dfs.replication</name>
                        <value>2</value>
                        </property>
                        <property>
                        <name>dfs.permissions</name>
                        <value>false</value>
                        </property>
                        </configuration>"""

    @property
    def mapred_site_text(self):
        return """<?xml version=\\""1.0\\"" encoding=\\""UTF-8\\""?>
                        <?xml-stylesheet type=\\""text/xsl\\"" href=\\""configuration.xsl\\""?>
                        <configuration>
                        <property>
                        <name>mapred.job.tracker</name>
                        <value>hdfs://{0}:8021</value>
                        </property>
                        </configuration>"""
