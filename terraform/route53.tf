resource "aws_route53_zone" "service" {
  name  = var.domain_name
}

resource "aws_route53_record" "service" {
  zone_id = var.tld_zone_id
  name    = var.domain_name
  type    = "NS"
  ttl     = 300
  records = [
    aws_route53_zone.service.name_servers[0],
    aws_route53_zone.service.name_servers[1],
    aws_route53_zone.service.name_servers[2],
    aws_route53_zone.service.name_servers[3]
  ]
}

resource "aws_route53_record" "service_record" {
  name    = "${var.domain_name}"
  type    = "A"
  zone_id = aws_route53_zone.service.id

  alias {
    # name                   = aws_cloudfront_distribution.default.domain_name
    # zone_id                = aws_cloudfront_distribution.default.hosted_zone_id
    name = aws_alb.alb.dns_name
    zone_id = aws_alb.alb.zone_id
    evaluate_target_health = false
  }
}