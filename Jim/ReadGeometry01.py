__author__ = 'mtacer'

import arcpy


def avg(values):
    sum = 0.0
    for n,v in enumerate(values, 1):
        sum += v
    # print Sum, n
    return sum / n

def corners(pnt_list):
    # calculate centroid
    pnt_centroid = (avg(x[0] for x in pnt_list), avg(x[1] for x in pnt_list))
    # print pnt_centroid

    north_points = [x for x in pnt_list if x[1] >= pnt_centroid[1]]
    north_min_x = min(x[0] for x in north_points)
    north_max_x = max(x[0] for x in north_points)

    south_points = [x for x in pnt_list if x[1] < pnt_centroid[1]]
    south_min_x = min(x[0] for x in south_points)
    south_max_x = max(x[0] for x in south_points)

    # extreme points
    points = {}
    try:
        points['NE'] = [pnt for pnt in north_points if pnt[0] == north_max_x][0] # north-east point
        points['NW'] = [pnt for pnt in north_points if pnt[0] == north_min_x][0] # north-west point
        points['SE'] = [pnt for pnt in south_points if pnt[0] == south_max_x][0] # south-east point
        points['SW'] = [pnt for pnt in south_points if pnt[0] == south_min_x][0] # south-west point
    except IndexError:
        print 'Cannot define corners of the shape: \n%s' % pnt_list
    return points

if __name__ == '__main__':
    infc = r'M:\USLandGrid\Indiana\Indiana.gdb\Section_Poly'
    where_clause = '\"OBJECTID\" = 34693'
    where_clause = '\"OBJECTID\" = 1104'
    print where_clause

    for i, row in enumerate(arcpy.da.SearchCursor(infc, ["OID@", "SHAPE@"], where_clause), 1):
        if i > 5: break

        print("Feature {0}:".format(row[0]))
        for part in row[1]:
            points = []
            for pnt in part:
                if pnt:
                    points.append((pnt.X, pnt.Y))
                    print("{0}, {1}".format(pnt.X, pnt.Y))
            print corners(points)
