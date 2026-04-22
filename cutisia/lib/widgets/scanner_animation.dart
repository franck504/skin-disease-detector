import 'package:flutter/material.dart';

class ScannerAnimation extends StatefulWidget {
  final bool visible;
  const ScannerAnimation({super.key, required this.visible});

  @override
  State<ScannerAnimation> createState() => _ScannerAnimationState();
}

class _ScannerAnimationState extends State<ScannerAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 3),
      vsync: this,
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedOpacity(
      opacity: widget.visible ? 1.0 : 0.0,
      duration: const Duration(milliseconds: 600),
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return CustomPaint(
            painter: _ScannerPainter(_controller.value),
            child: Container(),
          );
        },
      ),
    );
  }
}

class _ScannerPainter extends CustomPainter {
  final double progress;
  _ScannerPainter(this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final double y = size.height * progress;

    // --- 1. Grille digitale subtile ---
    final Paint gridPaint = Paint()
      ..color = const Color(0xFF2E5BFF).withValues(alpha: 0.06)
      ..strokeWidth = 0.5;
    const double step = 28.0;
    for (double i = 0; i <= size.width; i += step) {
      canvas.drawLine(Offset(i, 0), Offset(i, size.height), gridPaint);
    }
    for (double i = 0; i <= size.height; i += step) {
      canvas.drawLine(Offset(0, i), Offset(size.width, i), gridPaint);
    }

    // --- 2. Zone de lueur (glow) autour du laser ---
    final Paint glowPaint = Paint()
      ..shader = LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          const Color(0xFF2E5BFF).withValues(alpha: 0.0),
          const Color(0xFF2E5BFF).withValues(alpha: 0.18),
          const Color(0xFF2E5BFF).withValues(alpha: 0.0),
        ],
      ).createShader(Rect.fromLTWH(0, y - 50, size.width, 100));
    canvas.drawRect(Rect.fromLTWH(0, y - 50, size.width, 100), glowPaint);

    // --- 3. Ligne laser horizontale ---
    final Paint linePaint = Paint()
      ..shader = LinearGradient(
        colors: [
          Colors.transparent,
          const Color(0xFF2E5BFF).withValues(alpha: 0.6),
          const Color(0xFF7EB6FF),
          const Color(0xFF2E5BFF).withValues(alpha: 0.6),
          Colors.transparent,
        ],
        stops: const [0.0, 0.35, 0.5, 0.65, 1.0],
      ).createShader(Rect.fromLTWH(0, y - 2, size.width, 4))
      ..strokeWidth = 2.5
      ..style = PaintingStyle.stroke;
    canvas.drawLine(Offset(0, y), Offset(size.width, y), linePaint);

    // --- 4. Point lumineux au centre de la ligne ---
    final Paint dotPaint = Paint()
      ..color = Colors.white.withValues(alpha: 0.9)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4);
    canvas.drawCircle(Offset(size.width / 2, y), 4, dotPaint);
  }

  @override
  bool shouldRepaint(covariant _ScannerPainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}
