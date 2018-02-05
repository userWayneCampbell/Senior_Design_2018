﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Segment_Chooser
{
    public partial class Main : Form
    {
        public Main(String DateString = " ")
        {
            InitializeComponent();
            Console.WriteLine(Application.StartupPath);
            Console.WriteLine("\\" + DateString + "\\initial.png");
            Console.WriteLine(Application.StartupPath + "\\" + DateString + "\\initial.png");
            picOriginal.ImageLocation = Application.StartupPath + "\\" + DateString + "\\initial.png";
            picOriginal.Load();
        }

        // The original image.
        private Bitmap OriginalImage;

        // True when we're selecting a rectangle.
        private bool IsSelecting = false;

        // The area we are selecting.
        private int X0, Y0, X1, Y1;

        // Save the original image.
        private void Main_Load(object sender, EventArgs e)
        {
            OriginalImage = new Bitmap(picOriginal.Image);
        }

        private void picOriginal_MouseUp_1(object sender, MouseEventArgs e)
        {
            // Do nothing it we're not selecting an area.
            if (!IsSelecting) return;
            IsSelecting = false;

            // Display the original image.
            picOriginal.Image = OriginalImage;

            // Copy the selected part of the image.
            int wid = Math.Abs(X0 - X1);
            int hgt = Math.Abs(Y0 - Y1);
            if ((wid < 1) || (hgt < 1)) return;

            Bitmap area = new Bitmap(wid, hgt);
            using (Graphics gr = Graphics.FromImage(area))
            {
                Rectangle source_rectangle =
                    new Rectangle(Math.Min(X0, X1), Math.Min(Y0, Y1), wid, hgt);
                Rectangle dest_rectangle =
                    new Rectangle(0, 0, wid, hgt);
                gr.DrawImage(OriginalImage, dest_rectangle,
                    source_rectangle, GraphicsUnit.Pixel);
            }

            // Display the result.
            picResult.Image = area;
        }

        // Continue selecting.
        private void picOriginal_MouseMove_1(object sender, MouseEventArgs e)
        {
            // Do nothing it we're not selecting an area.
            if (!IsSelecting) return;

            // Save the new point.
            X1 = e.X;
            Y1 = e.Y;

            // Make a Bitmap to display the selection rectangle.
            Bitmap bm = new Bitmap(OriginalImage);

            // Draw the rectangle.
            using (Graphics gr = Graphics.FromImage(bm))
            {
                gr.DrawRectangle(Pens.Red,
                    Math.Min(X0, X1), Math.Min(Y0, Y1),
                    Math.Abs(X0 - X1), Math.Abs(Y0 - Y1));
            }

            // Display the temporary bitmap.
            picOriginal.Image = bm;
        }

        // Start selecting the rectangle.
        private void picOriginal_MouseDown_1(object sender, MouseEventArgs e)
        {
            IsSelecting = true;

            // Save the start point.
            X0 = e.X;
            Y0 = e.Y;
        }
    }
}
