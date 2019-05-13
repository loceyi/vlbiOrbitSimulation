# Import the library
from czml_local import CZML
from czml_local import CZMLPacket
from czml_local import Description
from czml_local import Billboard
from czml_local import Label
from czml_local import Path
from czml_local import Position
import shutil
import os

# Initialize a document

def CZML_Generate(Start_time,end_time,cartesian_file):

    doc = CZML()
    # Create and append the document packet
    packet1 = CZMLPacket(
        id="document",
        name = "simple",
        version= "1.0",
        clock= {
        "interval": "%s/%s"%(Start_time,end_time),
        "currentTime": "%s"%(Start_time),
        "multiplier": 60,
        "range": "LOOP_STOP",
        "step": "SYSTEM_CLOCK_MULTIPLIER"
    }
        )





    doc.packets.append(packet1)

    # Create and append a billboard packet
    packet2 = CZMLPacket(


        id="Satellite/VLBI_SAT",
        name="VLBI_SAT",
        availability="%s/%s"%(Start_time,end_time))

    pp=Position(interpolationDegree=5,
    interpolationAlgorithm="LAGRANGE",
    epoch="%s"%(Start_time))

    pp.cartesian=cartesian_file

    packet2.position=pp



    bb=Label(
          show=True,
          text="VLBI_SAT")

    bb.fillColor={
            "rgba":[
              0,255,0,255
            ]
          }
    bb.outlineColor={
            "rgba":[
              0,0,0,255
            ]
          }
    bb.pixelOffset={
            "cartesian2":[
              12,0
            ]
          }
    bb.font="11pt Lucida Console"
    bb.horizontalOrigin="LEFT"
    bb.outlineWidth=2
    bb.style="FILL_AND_OUTLINE"
    bb.verticalOrigin="CENTER"
    packet2.label = bb

    aa=Path(
          show=[
            {
              "interval":"%s/%s"%(Start_time,end_time),
              "boolean":True
            }
          ],
          width=1,
          material={
            "solidColor":{
              "color":{
                "rgba":[
                  0,255,0,255
                ]
              }
            }
          },
          resolution=120


        )

    aa.leadTime=[]
    # {
    #     "interval": "2012-03-15T10:00:00Z/2012-03-15T10:39:30.5752243210009Z",
    #     "epoch": "2012-03-15T10:00:00Z",
    #     "number": [
    #         0, 5903.376977238004,
    #         5903.376977238004, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T10:39:30.5752243210009Z/2012-03-15T12:17:53.9522015590046Z",
    #     "epoch": "2012-03-15T10:39:30.5752243210009Z",
    #     "number": [
    #         0, 5903.376977238004,
    #         5903.376977238004, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T12:17:53.9522015590046Z/2012-03-15T13:56:17.3309044399939Z",
    #     "epoch": "2012-03-15T12:17:53.9522015590046Z",
    #     "number": [
    #         0, 5903.378702880989,
    #         5903.378702880989, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T13:56:17.3309044399939Z/2012-03-15T15:34:40.7113328760024Z",
    #     "epoch": "2012-03-15T13:56:17.3309044399939Z",
    #     "number": [
    #         0, 5903.3804284360085,
    #         5903.3804284360085, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T15:34:40.7113328760024Z/2012-03-15T17:13:04.0934867610049Z",
    #     "epoch": "2012-03-15T15:34:40.7113328760024Z",
    #     "number": [
    #         0, 5903.3821538850025,
    #         5903.3821538850025, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T17:13:04.0934867610049Z/2012-03-15T18:51:27.4773659909988Z",
    #     "epoch": "2012-03-15T17:13:04.0934867610049Z",
    #     "number": [
    #         0, 5903.383879229994,
    #         5903.383879229994, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T18:51:27.4773659909988Z/2012-03-15T20:29:50.8629704579944Z",
    #     "epoch": "2012-03-15T18:51:27.4773659909988Z",
    #     "number": [
    #         0, 5903.385604466996,
    #         5903.385604466996, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T20:29:50.8629704579944Z/2012-03-15T22:08:14.6231253900041Z",
    #     "epoch": "2012-03-15T20:29:50.8629704579944Z",
    #     "number": [
    #         0, 5903.76015493201,
    #         5903.76015493201, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T22:08:14.6231253900041Z/2012-03-15T23:46:38.0402241229895Z",
    #     "epoch": "2012-03-15T22:08:14.6231253900041Z",
    #     "number": [
    #         0, 5903.417098732985,
    #         5903.417098732985, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T23:46:38.0402241229895Z/2012-03-16T01:25:01.45978897399618Z",
    #     "epoch": "2012-03-15T23:46:38.0402241229895Z",
    #     "number": [
    #         0, 5903.419564851007,
    #         5903.419564851007, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T01:25:01.45978897399618Z/2012-03-16T03:03:24.8818198189838Z",
    #     "epoch": "2012-03-16T01:25:01.45978897399618Z",
    #     "number": [
    #         0, 5903.422030844988,
    #         5903.422030844988, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T03:03:24.8818198189838Z/2012-03-16T04:41:48.3063165349886Z",
    #     "epoch": "2012-03-16T03:03:24.8818198189838Z",
    #     "number": [
    #         0, 5903.424496716005,
    #         5903.424496716005, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T04:41:48.3063165349886Z/2012-03-16T06:20:11.7332789999782Z",
    #     "epoch": "2012-03-16T04:41:48.3063165349886Z",
    #     "number": [
    #         0, 5903.42696246499,
    #         5903.42696246499, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T06:20:11.7332789999782Z/2012-03-16T07:58:35.1683124770061Z",
    #     "epoch": "2012-03-16T06:20:11.7332789999782Z",
    #     "number": [
    #         0, 5903.435033477028,
    #         5903.435033477028, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T07:58:35.1683124770061Z/2012-03-16T08:21:36.5644517090113Z",
    #     "epoch": "2012-03-16T07:58:35.1683124770061Z",
    #     "number": [
    #         0, 5903.435548290989,
    #         5903.435548290989, 0
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T08:21:36.5644517090113Z/2012-03-16T10:00:00Z",
    #     "epoch": "2012-03-16T08:21:36.5644517090113Z",
    #     "number": [
    #         0, 5903.435548290989,
    #         5903.435548290989, 0
    #     ]
    # }




    aa.trailTime=[]

    # {
    #     "interval": "2012-03-15T10:00:00Z/2012-03-15T10:39:30.5752243210009Z",
    #     "epoch": "2012-03-15T10:00:00Z",
    #     "number": [
    #         0, 0,
    #         5903.376977238004, 5903.376977238004
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T10:39:30.5752243210009Z/2012-03-15T12:17:53.9522015590046Z",
    #     "epoch": "2012-03-15T10:39:30.5752243210009Z",
    #     "number": [
    #         0, 0,
    #         5903.376977238004, 5903.376977238004
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T12:17:53.9522015590046Z/2012-03-15T13:56:17.3309044399939Z",
    #     "epoch": "2012-03-15T12:17:53.9522015590046Z",
    #     "number": [
    #         0, 0,
    #         5903.378702880989, 5903.378702880989
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T13:56:17.3309044399939Z/2012-03-15T15:34:40.7113328760024Z",
    #     "epoch": "2012-03-15T13:56:17.3309044399939Z",
    #     "number": [
    #         0, 0,
    #         5903.3804284360085, 5903.3804284360085
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T15:34:40.7113328760024Z/2012-03-15T17:13:04.0934867610049Z",
    #     "epoch": "2012-03-15T15:34:40.7113328760024Z",
    #     "number": [
    #         0, 0,
    #         5903.3821538850025, 5903.3821538850025
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T17:13:04.0934867610049Z/2012-03-15T18:51:27.4773659909988Z",
    #     "epoch": "2012-03-15T17:13:04.0934867610049Z",
    #     "number": [
    #         0, 0,
    #         5903.383879229994, 5903.383879229994
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T18:51:27.4773659909988Z/2012-03-15T20:29:50.8629704579944Z",
    #     "epoch": "2012-03-15T18:51:27.4773659909988Z",
    #     "number": [
    #         0, 0,
    #         5903.385604466996, 5903.385604466996
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T20:29:50.8629704579944Z/2012-03-15T22:08:14.6231253900041Z",
    #     "epoch": "2012-03-15T20:29:50.8629704579944Z",
    #     "number": [
    #         0, 0,
    #         5903.76015493201, 5903.76015493201
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T22:08:14.6231253900041Z/2012-03-15T23:46:38.0402241229895Z",
    #     "epoch": "2012-03-15T22:08:14.6231253900041Z",
    #     "number": [
    #         0, 0,
    #         5903.417098732985, 5903.417098732985
    #     ]
    # },
    # {
    #     "interval": "2012-03-15T23:46:38.0402241229895Z/2012-03-16T01:25:01.45978897399618Z",
    #     "epoch": "2012-03-15T23:46:38.0402241229895Z",
    #     "number": [
    #         0, 0,
    #         5903.419564851007, 5903.419564851007
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T01:25:01.45978897399618Z/2012-03-16T03:03:24.8818198189838Z",
    #     "epoch": "2012-03-16T01:25:01.45978897399618Z",
    #     "number": [
    #         0, 0,
    #         5903.422030844988, 5903.422030844988
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T03:03:24.8818198189838Z/2012-03-16T04:41:48.3063165349886Z",
    #     "epoch": "2012-03-16T03:03:24.8818198189838Z",
    #     "number": [
    #         0, 0,
    #         5903.424496716005, 5903.424496716005
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T04:41:48.3063165349886Z/2012-03-16T06:20:11.7332789999782Z",
    #     "epoch": "2012-03-16T04:41:48.3063165349886Z",
    #     "number": [
    #         0, 0,
    #         5903.42696246499, 5903.42696246499
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T06:20:11.7332789999782Z/2012-03-16T07:58:35.1683124770061Z",
    #     "epoch": "2012-03-16T06:20:11.7332789999782Z",
    #     "number": [
    #         0, 0,
    #         5903.435033477028, 5903.435033477028
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T07:58:35.1683124770061Z/2012-03-16T08:21:36.5644517090113Z",
    #     "epoch": "2012-03-16T07:58:35.1683124770061Z",
    #     "number": [
    #         0, 0,
    #         5903.435548290989, 5903.435548290989
    #     ]
    # },
    # {
    #     "interval": "2012-03-16T08:21:36.5644517090113Z/2012-03-16T10:00:00Z",
    #     "epoch": "2012-03-16T08:21:36.5644517090113Z",
    #     "number": [
    #         0, 0,
    #         5903.435548290989, 5903.435548290989
    #     ]
    # }



    packet2.path= aa

    dd=Description("<!--HTML-->\r\n<p>GeoEye-1 is a high-resolution earth observation satellite owned by GeoEye, which was launched in September 2008.</p>\r\n\r\n<p>On December 1, 2004, General Dynamics C4 Systems announced it had been awarded a contract worth approximately $209 million to build the OrbView-5 satellite. Its sensor is designed by the ITT Exelis.</p>\r\n\r\n<p>The satellite, now known as GeoEye-1, was originally scheduled for April 2008 but lost its 30-day launch slot to a U.S. government mission which had been delayed. It was rescheduled for launch August 22, 2008 from Vandenberg Air Force Base aboard a Delta II launch vehicle. The launch was postponed to September 4, 2008, due to unavailability of the Big Crow telemetry-relay aircraft. It was delayed again to September 6 because Hurricane Hanna interfered with its launch crews.</p>\r\n\r\n<p>The launch took place successfully on September 6, 2008 at 11:50:57 a.m. PDT (18:50:57 UTC). The GeoEye-1 satellite separated successfully from its Delta II launch vehicle at 12:49 p.m. PDT (19:49 UTC), 58 minutes and 56 seconds after launch.</p>",)
    packet2.description=dd



    cc=Billboard(scale=1.5,
          show=True)
    cc.eyeOffset={
       "cartesian":[
              0,0,0
            ]
          }
    cc.horizontalOrigin="CENTER"
    cc.image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
    cc.pixelOffset={
            "cartesian2":[
              0,0
            ]
          }
    cc.verticalOrigin="CENTER"
    cc.color = {}
    packet2.billboard = cc





    doc.packets.append(packet2)

    # Write the CZML document to a file
    filename = "satellite.czml"
    doc.write(filename)
    old_path=os.getcwd()
    new_path='Cesium/Orbit_Simulation_GUI/SampleData'
    shutil.copyfile(os.path.join(old_path,filename),os.path.join(new_path,filename))#路径拼接要用os.path.join，复制指定文件到另一个文件夹里

    os.remove(os.path.join(old_path,filename))#删除原文件夹中的指定文件文件

    return


def test_CZML():
    from Hpop_test import HPOP
    Start_time="2012-03-15T10:00:00Z"
    end_time="2012-03-16T10:00:00Z"
    position, time = HPOP()
    x=position[0,:]
    y=position[1,:]
    z=position[2,:]

    time=time.tolist()
    cartesian_file=[]
    for i in range(0,len(time)):

        cartesian_file.append(time[i])
        cartesian_file.append(x[i])
        cartesian_file.append(y[i])
        cartesian_file.append(z[i])





    CZML_Generate(Start_time,end_time,cartesian_file)


if __name__ == "__main__":
    test_CZML()
    print('1')