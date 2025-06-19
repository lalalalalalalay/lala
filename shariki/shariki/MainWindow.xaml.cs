using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Shapes;
using System.Windows.Media;
using System.Threading;
using System.Windows.Controls;

namespace BallCollisionWPF
{
    public partial class MainWindow : Window
    {
        private const double BallRadius = 15;
        private const double TimeStep = 0.016; // ~60 FPS
        private readonly List<Ball> _balls = new List<Ball>();
        private readonly DatabaseService _db = new DatabaseService(
            "Host=localhost;Port=5432;Username=postgres;Password=your_new_password;Database=ballsdb");
        private bool _running;

        public MainWindow()
        {
            InitializeComponent();
            this.Loaded += MainWindow_Loaded;
            this.Closing += (s, e) => _running = false;
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            _running = true;
            LoadBallsFromDatabase();
            StartBallThreads();
        }

        private void LoadBallsFromDatabase()
        {
            var positions = _db.LoadInitialPositions();
            var rand = new Random();

            foreach (var pt in positions)
            {
                var ball = new Ball
                {
                    X = pt.X,
                    Y = pt.Y,
                    VX = rand.NextDouble() * 100 - 50,
                    VY = rand.NextDouble() * 100 - 50,
                    Radius = BallRadius,
                    UIElement = new Ellipse
                    {
                        Width = BallRadius * 2,
                        Height = BallRadius * 2,
                        Fill = Brushes.Cyan
                    }
                };
                _balls.Add(ball);
                SimulationCanvas.Children.Add(ball.UIElement);
                // Initial placement
                Canvas.SetLeft(ball.UIElement, ball.X - BallRadius);
                Canvas.SetTop(ball.UIElement, ball.Y - BallRadius);
            }
        }

        private void StartBallThreads()
        {
            foreach (var ball in _balls)
            {
                var thread = new Thread(() => BallLoop(ball))
                {
                    IsBackground = true
                };
                thread.Start();
            }
        }

        private void BallLoop(Ball ball)
        {
            while (_running)
            {
                PhysicsService.ApplyForces(
                    ball,
                    _balls,
                    SimulationCanvas.ActualWidth,
                    SimulationCanvas.ActualHeight,
                    TimeStep);

                // Update UI
                try
                {
                    Dispatcher.Invoke(() =>
                    {
                        double canvasWidth = SimulationCanvas.ActualWidth;
                        double canvasHeight = SimulationCanvas.ActualHeight;
                        double left = ball.X - ball.Radius;
                        double top = ball.Y - ball.Radius;

                        // Clamp within bounds
                        if (canvasWidth > BallRadius * 2)
                        {
                            left = Math.Max(0, Math.Min(left, canvasWidth - BallRadius * 2));
                        }
                        if (canvasHeight > BallRadius * 2)
                        {
                            top = Math.Max(0, Math.Min(top, canvasHeight - BallRadius * 2));
                        }

                        Canvas.SetLeft(ball.UIElement, left);
                        Canvas.SetTop(ball.UIElement, top);
                    });
                }
                catch (Exception)
                {
                    // Игнорируем ошибки установки позиции
                }

                Thread.Sleep((int)(TimeStep * 1000));
            }
        }
    }
}
