# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 21:56:37 2023

@author: Robert Stuckey
"""
import tkinter as tk
class point():
    points=[]
    def __init__(self,x,y):
        r=2
        self.xvalue=x
        self.yvalue=y
        self.widget=canvas.create_oval(x+r,y+r,x-r,y-r,fill="green",outline="green")
        self.__class__.points.append(self)
class tile():
    tiles=[]
    def __init__(self,P1,size=10,edges=False,color="white"):
        self.contents=[]
        self.widget=canvas.create_rectangle(canvas,P1.xvalue,P1.yvalue,P1.xvalue+size,P1.yvalue+size)

root=tk.Tk()
root.title("Collider Test")

root.geometry("720x720")
root.resizable(True,True)
canvas=tk.Canvas(root,bg="white",height=720,width=720)

P=point(100,100)
canvas.pack()
root.mainloop()