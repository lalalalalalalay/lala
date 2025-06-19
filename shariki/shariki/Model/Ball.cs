using System.Windows.Shapes;

namespace BallCollisionWPF
{
    public class Ball
    {
        public double X { get; set; }
        public double Y { get; set; }
        public double VX { get; set; }
        public double VY { get; set; }
        public double Radius { get; set; }
        public Ellipse UIElement { get; set; }
    }
}