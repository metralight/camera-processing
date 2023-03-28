import pprint
import time
import os
import cv2
import numpy as np
import logging
import sys

class CameraImg:

    def __init__( self, img_src, pixel_size, treshold_proc, maxWidth, maxHeight, center_x_um=0, center_y_um=0):
        self.pixel_size = pixel_size
        self.treshold_proc = treshold_proc
        self.center_x_um = center_x_um
        self.center_y_um = center_y_um

        self.resizeFactor, self.img_src = self.resizeToMaxDimensions(img_src, maxWidth, maxHeight)
        self.cut_horizontal = np.zeros((280, self.img_src.shape[1], 3))
        self.cut_vertical = np.zeros((280, self.img_src.shape[0], 3))

        self.img_dst = np.copy(self.img_src)

        # neni nutne - jeste nasleduce gaussian na img_gray
        # self.img_src = cv2.medianBlur(self.img_src, 5)

        self.img_gray = cv2.cvtColor(self.img_src, cv2.COLOR_BGR2GRAY)
        self.img_gray = cv2.GaussianBlur(self.img_gray, (25,25), 0)

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(self.img_gray)
        print("maxVal:" + str(maxVal))
        #print("maxLoc:" + str(maxLoc))
        #cv2.circle(self.img_gray, maxLoc, 5, (255, 0, 0), 2)

        th = maxVal - (maxVal/100.*self.treshold_proc)
        ret, self.img_calc = cv2.threshold(self.img_gray,th,maxVal,cv2.THRESH_TOZERO)

        self.centroid_x_px = None
        self.centroid_y_px = None
        self.centroid_center_dist_x_px = 0
        self.centroid_center_dist_y_px = 0

        self.beam_width_px = 0
        self.beam_height_px = 0
        self.beam_height_top_px = 0
        self.beam_width_left_px = 0
        self.beam_volume_px = 0

        self.line_width = 1
        self.line_width_centroid_cut = 1
        self.font_size = 0.3
        self.font_line_width = 1

    def resizeToMaxDimensions(self, image, maxWidth, maxHeight):
        f1 = maxWidth / image.shape[1]
        f2 = maxHeight / image.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(image.shape[1] * f), int(image.shape[0] * f))
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return f, resized
    
    def pixToUm(self, pixVal):
        return pixVal * (self.pixel_size / self.resizeFactor)
    
    def process( self ):
        self.get_centroid_pos()
        #self.img_gray[self.img_gray<50] = 0
        #self.img_gray[self.img_gray>=50] -= 50
        #cv2.normalize(self.img_gray,self.img_gray,0,255,cv2.NORM_MINMAX)
        ##hsv = np.full((1200,1920,3),255,"uint16")
        w = self.img_src.shape[0]
        h = self.img_src.shape[1]
        hsv = np.full((w,h,3),255,"uint16")
        hsv[:,:,0] = ((255-self.img_gray.astype("uint16"))*160/256+150)%180
        hsv[:,:,2] = np.sqrt(self.img_gray.astype("uint16"))*16
        self.img_dst = cv2.cvtColor(hsv.astype("uint8"),cv2.COLOR_HSV2BGR)
        if self.centroid_x_px is not None:
            self.draw_measures()
            self.draw_centroid()
            self.draw_centroid_cut()
            self.calc_beam_size() #nakonec - zavisi na centroidu
            # self.draw_beam_size()
        else:
            cv2.putText(self.img_dst, "Centroid not found.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def get_calculated_data(self):
        return {
            'centroid_x_px' : self.centroid_x_px if self.centroid_x_px is not None else 0,
            'centroid_y_px' : self.centroid_y_px if self.centroid_y_px is not None else 0,
            'centroid_center_dist_x_px' : self.centroid_center_dist_x_px,
            'centroid_center_dist_y_px' : self.centroid_center_dist_y_px,
            'centroid_center_dist_x_um'  : round(self.pixToUm(self.centroid_center_dist_x_px)-self.center_x_um),
            'centroid_center_dist_y_um'  : round(self.pixToUm(self.centroid_center_dist_y_px)-self.center_y_um),
            'beam_width_px' : self.beam_width_px,
            'beam_height_px' : self.beam_height_px,
            'beam_width_um' : round(self.pixToUm(self.beam_width_px)),
            'beam_height_um' : round(self.pixToUm(self.beam_height_px)),
            'beam_volume_px' : self.beam_volume_px,
        }

    def get_centroid_pos( self ):
        # calculate moments of binary image
        M = cv2.moments(self.img_calc)
        if M["m00"] > 0:
            # calculate x,y coordinate of center
            self.centroid_x_px = int(M["m10"] / M["m00"])
            self.centroid_y_px = int(M["m01"] / M["m00"])

            w = self.img_calc.shape[1]
            h = self.img_calc.shape[0]
            self.centroid_center_dist_x_px = -((w / 2) - self.centroid_x_px)
            self.centroid_center_dist_y_px = (h / 2) - self.centroid_y_px


    def calc_beam_size( self ):
        w = self.img_gray.shape[1]
        h = self.img_gray.shape[0]
        bw = 0
        for i in range( self.centroid_x_px, 0, -1 ):
            if self.img_gray[self.centroid_y_px][i] < 128:
                break
            self.beam_width_left_px = i
            bw += 1
        for i in range( self.centroid_x_px, w, 1 ):
            if self.img_gray[self.centroid_y_px][i] < 128:
                break
            bw += 1
        self.beam_width_px = bw

        bh = 0
        for i in range( self.centroid_y_px, 0, -1 ):
            if self.img_gray[i][self.centroid_x_px] < 128:
                break
            self.beam_height_top_px = i
            bh += 1
        for i in range( self.centroid_y_px, h, 1 ):
            if self.img_gray[i][self.centroid_x_px] < 128:
                break
            bh += 1
        self.beam_height_px = bh

        x1 = self.beam_width_left_px
        x2 = self.beam_width_left_px + self.beam_width_px
        y1 = self.beam_height_top_px
        y2 = self.beam_height_top_px + self.beam_height_px
        # beam volume vypnute
        # aa = self.img_gray[y1:y2,x1:x2]
        # self.beam_volume_px = np.sum(aa)

    def draw_centroid( self ):
        if self.centroid_x_px is not None:
            h = self.img_dst.shape[0]
            w = self.img_dst.shape[1]
            cv2.line(self.img_dst, (0,self.centroid_y_px), (w,self.centroid_y_px), (170,170,170), self.line_width) 
            cv2.line(self.img_dst, (self.centroid_x_px,0), (self.centroid_x_px,h), (170,170,170), self.line_width) 


    def draw_centroid_cut( self ):
        if self.centroid_x_px is None:
            return
        
        h = self.img_src.shape[0]
        w = self.img_src.shape[1]
        lx = []
        ly = []

        # nejrpve mrizka, pak signal
        self.draw_measures_cut(self.cut_horizontal)
        self.draw_measures_cut(self.cut_vertical)

        # TO DO optimalizovat z cyklu
        for x in range(0,w):
            lx.append(self.img_gray[self.centroid_y_px][x])
        for y in range(0,h):
            ly.append(self.img_gray[y][self.centroid_x_px])

        for x in range(0,w-1):
            #self.img_dst[lx[x]][x] = (0,255,0)
            cv2.line(self.cut_horizontal, (x,self.cut_horizontal.shape[0]-lx[x]), (x+1,self.cut_horizontal.shape[0]-lx[x+1]), (255, 255, 255), self.line_width_centroid_cut) 
        for y in range(0,h-1):
            #self.img_dst[y][ly[y]] = (0,0,255 )
            cv2.line(self.cut_vertical, (y, self.cut_vertical.shape[0]-ly[y]), (y+1, self.cut_vertical.shape[0]-ly[y+1]), (255, 255, 255), self.line_width_centroid_cut) 

        # cv2.imshow("v", self.cut_vertical)
        # cv2.imshow("h", self.cut_horizontal)
        # cv2.waitKey(100)

    def draw_beam_size( self ):
        if self.centroid_x_px is None:
            return
        cv2.rectangle(self.img_dst,
                (self.beam_width_left_px,self.beam_height_top_px),
                (self.beam_width_left_px+self.beam_width_px,self.beam_height_top_px+self.beam_height_px),
                (255,255,255),2) 

    def draw_measures( self ):
        if self.centroid_x_px is None:
            return
        h = self.img_dst.shape[0]
        w = self.img_dst.shape[1]

        zero_x = -1*round(self.center_x_um/(self.pixel_size/self.resizeFactor))
        zero_y = -1*round(self.center_y_um/(self.pixel_size/self.resizeFactor))

        #cross
        #cv2.line(self.img_dst, (int(w/2)+zero_x,0), (int(w/2)+zero_x,h), (150,150,150), self.line_width) 
        #cv2.line(self.img_dst, (0,int(h/2)+zero_y), (w,int(h/2)+zero_y), (150,150,150), self.line_width) 
        cross_sz = int(h / 40 )
        meas_big_line_size = int(h / 80 )
        cv2.line(self.img_dst, (int(w/2)+zero_x,int(h/2)+zero_y-cross_sz), (int(w/2)+zero_x,int(h/2)+zero_y+cross_sz), (255,255,255), self.line_width) 
        cv2.line(self.img_dst, (int(w/2)+zero_x-cross_sz,int(h/2)+zero_y), (int(w/2)+zero_x+cross_sz,int(h/2)+zero_y), (255,255,255), self.line_width) 

        # nezaokrouhlovat! - zaokrouhlit az uvnitr pred vykreslenim
        # ve for cyklu pokud se pouzije zaokrouhlene jako step, tak se vyscita chyba
        big_step = 1000/(self.pixel_size/self.resizeFactor)
        small_step = big_step / 10

        #label = ((int(self.centroid_x_px / big_step) + 1) * -1000)
        #start = (self.centroid_x_px % big_step) - big_step
        #label = ((int((w/2) / big_step) + 1) * -1000)
        #start = int(((w/2) % big_step) - big_step)
        label = (int(((w/2)+zero_x) / big_step) + 1) * -1000 #pocitaji se cele dilky, musi byt floor
        start = round((((w/2)+zero_x) % big_step) - big_step)
        for i in np.arange(start,w,big_step):
            x = round(i)
            cv2.line(self.img_dst, (x,w), (x,h-meas_big_line_size), (255,255,255), self.line_width) 
            txt_sz = cv2.getTextSize(str(label), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, self.font_line_width)
            cv2.putText(self.img_dst, str(label), (int(x - txt_sz[0][0]/2), h - (meas_big_line_size + 5)),cv2.FONT_HERSHEY_SIMPLEX, self.font_size, (255, 255, 255), self.font_line_width)
            cnt = 0
            # kratke carky - kazda pata vetsi
            # zaokrouhlit az uvnitr cyklu po prenasobeni
            for j in range(10):
                x2 = round(j * small_step)
                ln_len = meas_big_line_size if cnt == 5 else int(meas_big_line_size / 2)
                cv2.line(self.img_dst, (x+x2,w), (x+x2,h-ln_len), (255,255,255), self.line_width) 
                cnt += 1
            label += 1000

        #label = (int(self.centroid_y_px / big_step) + 1) * -1000
        #start = (self.centroid_y_px % big_step) - big_step
        #label = (int((h/2) / big_step) + 1) * -1000
        #start = int(((h/2) % big_step) - big_step)

        label = (int(((h/2)+zero_y) / big_step) + 1) * + 1000 #pocitaji se cele dilky, musi byt floor
        start = int((((h/2)+zero_y) % big_step) - big_step)
        for i in np.arange(start,h,big_step):
            y = round(i)
            cv2.line(self.img_dst, (0,y), (meas_big_line_size,y), (255,255,255), self.line_width) 
            txt_sz = cv2.getTextSize(str(label), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, self.font_line_width)
            cv2.putText(self.img_dst, str(label), (meas_big_line_size+5, int(y + txt_sz[0][1]/2)),cv2.FONT_HERSHEY_SIMPLEX, self.font_size, (255, 255, 255), self.font_line_width)
            cnt = 0
            # kratke carky - kazda pata vetsi
            for j in range(10):
                y2 = round(j * small_step)
                ln_len = meas_big_line_size if cnt == 5 else int(meas_big_line_size / 2)
                cv2.line(self.img_dst, (0,y+y2), (ln_len,y+y2), (255,255,255), self.line_width) 
                cnt += 1
            label -= 1000

    def draw_measures_cut(self, target):
        if self.centroid_x_px is None:
            return
        
        h = target.shape[0]
        w = target.shape[1]

        zero_x = -1*round(self.center_x_um/(self.pixel_size/self.resizeFactor))

        # nezaokrouhlovat! - zaokrouhlit az uvnitr pred vykreslenim
        # ve for cyklu pokud se pouzije zaokrouhlene jako step, tak se vyscita chyba
        big_step = 1000/(self.pixel_size/self.resizeFactor)
        small_step = big_step / 10

        color = (90, 90, 90)
        meas_big_line_size = 14

        # horizontalne mikrony jako na obrazu
        label = ((int(((w/2)+zero_x) / big_step) + 1) * - 1000)
        start = round((((w/2)+zero_x) % big_step) - big_step)
        for i in np.arange(start,w,big_step):
            x = round(i)
            cv2.line(target, (x,0), (x,h), color, self.line_width) 
            txt_sz = cv2.getTextSize(str(label), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, self.font_line_width)
            cv2.putText(target, str(label), (x+3, h - txt_sz[0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, color, self.font_line_width)
            # kratke carky - kazda pata vetsi
            cnt = 0
            for j in range(10):
                x2 = round(j * small_step)
                ln_len = meas_big_line_size if cnt == 5 else int(meas_big_line_size / 2)
                cv2.line(target, (x+x2,w), (x+x2,h-ln_len), color, self.line_width) 
                cnt += 1
            label += 1000

        # vertikalne intenzita svetla 
        label = 50
        start = 0
        for y in range(start, 255, 50):
            cv2.line(target, (0,h-y), (w,h-y), color, self.line_width) 
            txt_sz = cv2.getTextSize(str(label), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, self.font_line_width)
            cv2.putText(target, str(y), (2, int(h - (y + txt_sz[0][1] + 2))), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, color, self.font_line_width)


    def draw_info( self, print_info ):
        h = self.img_dst.shape[0]
        w = self.img_dst.shape[1]
        title_x = w - 300
        val_x = title_x + 170
        y_step = 20
        y = y_step
        for it in print_info:
            cv2.putText(self.img_dst, str(it[0]), (title_x, y),cv2.FONT_HERSHEY_SIMPLEX, self.font_size, it[2], self.font_line_width)
            cv2.putText(self.img_dst, str(it[1]), (val_x, y),cv2.FONT_HERSHEY_SIMPLEX, self.font_size, it[2], self.font_line_width)
            y += y_step

    def draw_info_small( self, txt, col ):
        cv2.putText(self.img_dst, str(txt), (20, 10),cv2.FONT_HERSHEY_SIMPLEX, 0.4, col, 1)

    def get_graph_surface_data( self ):
            small = cv2.resize(self.img_gray, (60, 60)) 
            h = small.shape[0]
            w = small.shape[1]
            out = []
            for y in range(0,h):
                rr = []
                for x in range(0,w):
                    rr.append(small[y][x])
                out.append(rr)
            return out


def img_resize( img, sz = 1 ):
    return cv2.resize(img, (0,0), fx=sz, fy=sz) 

if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    ci = CameraImg( img, 5.86, 15, -200, -200 )
    #cv2.imshow("Image", img_resize(img,0.3))
    #cv2.waitKey(0)
    ret = ci.process()
    calc_data = ci.get_calculated_data()
    print("calc_data:" + str(calc_data))

    zoom = 1
    #cv2.imshow("Image", img_resize(ci.img_dst,self.font_size))

    cv2.imshow("Image", img_resize(img,zoom))
    cv2.waitKey(0)
    #cv2.imshow("Image", img_resize(ci.img_src,zoom))
    #cv2.waitKey(0)
    cv2.imshow("Image", img_resize(ci.img_gray,zoom))
    cv2.waitKey(0)
    cv2.imshow("Image", img_resize(ci.img_dst,zoom))
    cv2.waitKey(0)



