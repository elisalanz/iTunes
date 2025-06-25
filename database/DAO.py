from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAlbums(dMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)
        query = """SELECT a.*, SUM(t.Milliseconds)/1000/60 as dTot 
                    FROM album a, track t
                    WHERE a.AlbumId = t.AlbumId
                    GROUP BY a.AlbumId
                    HAVING dTot > %s
                    """
        cursor.execute(query, (dMin,)) # durata in minuti
        results = []
        for row in cursor:
            results.append(Album(**row))
        cursor.close()
        cnx.close()
        return results

    @staticmethod
    def getAllEdges(idMapAlbum):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT t1.AlbumId as a1, t2.AlbumId as a2
                   FROM track t1, track t2, playlisttrack p1, playlisttrack p2
                   WHERE t2.TrackId = p2.TrackId AND t1.TrackId = p1.TrackId AND p2.PlaylistId = p1.PlaylistId
                   AND t1.AlbumId < t2.AlbumId
                   """
        cursor.execute(query)
        results = []
        for row in cursor:
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
                results.append((idMapAlbum[row["a1"]], idMapAlbum[row["a2"]])) # tuple di nodi
        cursor.close()
        cnx.close()
        return results