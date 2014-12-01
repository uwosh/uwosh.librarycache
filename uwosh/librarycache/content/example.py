from uwosh.librarycache.core import CacheCore

class Dummy(CacheCore):
    """
    This is an example.  Implement build();  Add any other 
    functionality you need to do your build.
    
    Make sure build 'returns' something (your content).
    
    Also make sure to register the Adapter name in propertiestool.xml
    - See propertiestools.xml in this product.
    
    The name should be the same as your configure.zcml adapters name.
          <adapter factory=".example.Dummy"
             name="DummyCache" />
             
    - See content/configure.zcml in this product.
    """
    
    def build(self):
        return ["1","2","5","Three Sir!","THREE!"]